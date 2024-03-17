# In this file we generate nodes using llamaindex
# and populate the EdgeDB with the nodes.

from llama_index.core import SimpleDirectoryReader

from llama_index.core.node_parser import (
    HierarchicalNodeParser,
    SentenceSplitter,
    TokenTextSplitter,
)

from llama_index.core.extractors import (
    SummaryExtractor,
    QuestionsAnsweredExtractor,
    BaseExtractor,
    TitleExtractor,
    KeywordExtractor,
)

import nest_asyncio
nest_asyncio.apply()

from llama_index.extractors.entity import EntityExtractor
from llama_index.core.ingestion import IngestionPipeline
from llama_index.llms.openai import OpenAI
from llama_index.core.schema import MetadataMode

import os
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
llm = OpenAI(temperature=0.1, model="gpt-4-turbo-preview", max_tokens=512)

#extract nodes first time
documents = SimpleDirectoryReader("/Users/yangyue/Desktop/textbooks").load_data()
node_parser = HierarchicalNodeParser.from_defaults()
nodes = node_parser.get_nodes_from_documents(documents)

#extract metadata to boost search
class CustomExtractor(BaseExtractor):
    def extract(self, nodes):
        metadata_list = [
            {
                "custom": (
                    node.metadata["document_title"]
                    + "\n"
                    + node.metadata["excerpt_keywords"]
                )
            }
            for node in nodes
        ]
        return metadata_list


extractors = [
    TitleExtractor(nodes=5, llm=llm),
    QuestionsAnsweredExtractor(questions=3, llm=llm),
    EntityExtractor(prediction_threshold=0.5),
    SummaryExtractor(summaries=["prev", "self"], llm=llm),
    KeywordExtractor(keywords=10, llm=llm)
]

text_splitter = TokenTextSplitter(
    separator=" ", chunk_size=512, chunk_overlap=128
)

transformations = [text_splitter] + extractors

# process nodes with metadata extractors, the nodes are ready to put in Edgedb
pipeline = IngestionPipeline(transformations=transformations)
nodes = pipeline.run(nodes=nodes, in_place=False, show_progress=True)

#get all leaf nodes
from llama_index.core.node_parser import get_leaf_nodes, get_root_nodes
leaf_nodes = get_leaf_nodes(nodes)
root_nodes = get_root_nodes(nodes)

#ingest nodes 
import edgedb
client = edgedb.create_client()
def insert_text_nodes(nodes):
    for text_node in nodes:
        source = text_node.metadata['file_name']  # Assuming 'source' comes from 'file_name'
        
        questionsThisExcerptCanAnswer = []
        entities = []
        prevSectionSummary = ""
        sectionSummary = ""
        excerptKeywords = []
        
        # Initialize the dictionary for optional query parameters
        optional_values = {
            "id": text_node.id_,
            "source": source,
            "questionsThisExcerptCanAnswer": questionsThisExcerptCanAnswer,
            "entities": entities,
            "prevSectionSummary": prevSectionSummary,
            "sectionSummary": sectionSummary,
            "excerptKeywords": excerptKeywords,
            "text": text_node.text
        }

        # Conditionally add optional fields to the query and parameters
        optional_parts = []
        if text_node.start_char_idx is not None:
            optional_parts.append("startCharIdx := <int64>$startCharIdx")
            optional_values["startCharIdx"] = text_node.start_char_idx

        if text_node.end_char_idx is not None:
            optional_parts.append("endCharIdx := <int64>$endCharIdx")
            optional_values["endCharIdx"] = text_node.end_char_idx
        
        optional_query_part = ", ".join(optional_parts)
        
        query = f"""
        INSERT TextNode {{
            textNodeId := <str>$id,
            source := <str>$source,
            questionsThisExcerptCanAnswer := <array<str>>$questionsThisExcerptCanAnswer,
            entities := <array<str>>$entities,
            prevSectionSummary := <str>$prevSectionSummary,
            sectionSummary := <str>$sectionSummary,
            excerptKeywords := <array<str>>$excerptKeywords,
            text := <str>$text,
            {optional_query_part}
        }};
        """
        
        client.query(query, **optional_values)
        print(f"TextNode {text_node.id_} inserted successfully.")


insert_text_nodes(nodes)