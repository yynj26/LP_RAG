
from sklearn.neighbors import NearestNeighbors
import numpy as np
from nodes_ import nodes

def fetch_and_embed_nodes():
    embeddings = np.random.rand(len(nodes), len(nodes))  
    return nodes, embeddings

# Function to index embeddings
def index_embeddings(embeddings):
    # Using NearestNeighbors from scikit-learn for simplicity
    nn = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(embeddings)
    return nn

# Querying embeddings and retrieving the closest node
def query_embeddings(query_embedding, nn, nodes):
    # Find the nearest node embedding to the query_embedding
    distances, indices = nn.kneighbors([query_embedding])
    closest_node_index = indices[0][0]
    closest_node = nodes[closest_node_index]
    return closest_node

nodes, embeddings = fetch_and_embed_nodes()
nn_index = index_embeddings(embeddings)


#Queury functions
def generate_embedding_for_query(query):
    query_embedding = np.random.rand(1, len(nodes))  # Adjust dimensions as needed
    return query_embedding

# Function to retrieve the top 3 related nodes based on the query embedding
def retrieve_related_nodes(query_embedding, nn, nodes):
    distances, indices = nn.kneighbors(query_embedding)
    closest_nodes_indices = indices[0]
    closest_nodes = [nodes[i] for i in closest_nodes_indices]
    return closest_nodes


