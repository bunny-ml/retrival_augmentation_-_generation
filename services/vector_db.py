import os
import chromadb
from langchain_chroma import Chroma
from langchain_community.embeddings import JinaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

chroma_key = os.getenv("chroma_key")
chroma_tenant = os.getenv("tenant")

jina_key = os.getenv('jina_key')


cloud_client = chromadb.CloudClient(
    api_key=chroma_key,
    tenant=chroma_tenant,
    database='RAG'
)

embeddings = JinaEmbeddings(
    jina_api_key=jina_key, 
    model_name="jina-embeddings-v2-base-en" 
)

vector_store = Chroma(
    client=cloud_client,
    collection_name="jina_verified_v1", 
    embedding_function=embeddings
)

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)