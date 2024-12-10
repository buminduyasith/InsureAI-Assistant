from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_postgres.vectorstores import PGVector
import os
from dotenv import load_dotenv

load_dotenv()
def loadData():

    openai_api_key = os.getenv('OPENAI_API_KEY')
    loader = PyPDFLoader(file_path="test.pdf")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
            )
    
    splitsdocs = text_splitter.split_documents(documents)
    
    embeddings = OpenAIEmbeddings(
        openai_api_key = openai_api_key
    )

    connection = "postgresql+psycopg://langchain:langchain@localhost:6024/langchain"  # Uses psycopg3!
    collection_name = "my_docs"

    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=connection,
        use_jsonb=True,
    )

    vector_store.add_documents(splitsdocs)



def getData(query):
    openai_api_key = os.getenv('OPENAI_API_KEY')
    embeddings = OpenAIEmbeddings(
        openai_api_key=openai_api_key
    )

    connection = "postgresql+psycopg://langchain:langchain@localhost:6024/langchain"  # Uses psycopg3!
    collection_name = "my_docs"

    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=connection,
        use_jsonb=True,
    )
    docs = vector_store.similarity_search(query, k=5)

    for doc in docs:
        print(doc.page_content)

loadData()