from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import PGVector
import tqdm


def loadData():

    # Load the PDF
    loader = PyPDFLoader(file_path="test.pdf")
    documents = loader.load()

    # Chunk the text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", "  "]
    )
    docs = text_splitter.split_documents(documents)

    # Create embeddings
    embeddings = OpenAIEmbeddings(
        openai_api_key="")

    # Connect to Postgres Vector DB
    pgvector = PGVector(
        connection_string="postgresql://postgres:password123@localhost:5432/your_database",
        embedding_function=embeddings
    )

    # Add documents to the vector store with a progress bar
    for i in tqdm.tqdm(range(0, len(docs), 100)):
        batch = docs[i:i+100]
        pgvector.add_documents(batch)


query = "What is the Coverage Amount?"

embeddings = OpenAIEmbeddings(
    openai_api_key="")

pgvector = PGVector(
    connection_string="postgresql://postgres:password123@localhost:5432/your_database",
    embedding_function=embeddings
)
# Search the vector store
docs = pgvector.similarity_search(query, k=1)

# Print the relevant text
for doc in docs:
    print(doc.page_content)
