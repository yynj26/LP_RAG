#This is the chatbot ui with output generated by perplexity.

import streamlit as st
from openai import OpenAI
import os
from query import generate_embedding_for_query,retrieve_related_nodes
from dotenv import load_dotenv


# Initialize the sidebar for API key input
with st.sidebar:
    perplexity_api_key = st.text_input("Perplexity API Key", key="chatbot_api_key", type="password")
    st.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
    st.markdown("[View the source code](https://github.com/yynj26/LP_RAG)")
    st.markdown("[View the knowledge graph](http://localhost:10707/ui/edgedb/schema)")

st.title("Linear Programming Chatbot")

# Initialize or retrieve the conversation history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "How can I help you?"}]

# Display the chat history
for msg in st.session_state.messages:
    if msg["role"] in ["user", "assistant"]:
        st.chat_message(role=msg["role"]).write(msg["content"])

load_dotenv()
perplexity_api_key = os.getenv('perplexity_api_key')

# Input from the user
if prompt := st.chat_input():
    if not perplexity_api_key:
        st.info("Please add your Perplexity API key to continue.")
    else:
        # Append the user message
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Initialize the OpenAI client
        client = OpenAI(api_key=perplexity_api_key, base_url="https://api.perplexity.ai")

        try:
            # Generate a response from the model
            response = client.chat.completions.create(
                model="codellama-70b-instruct",
                messages=[msg for msg in st.session_state.messages if msg["role"] in ["user", "assistant"]]
            )
            msg = response.choices[0].message.content

            # Append the assistant's response
            st.session_state.messages.append({"role": "assistant", "content": msg})

            # Display the response
            st.chat_message("assistant").write(msg)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
