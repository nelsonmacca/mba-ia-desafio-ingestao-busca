
import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_postgres.vectorstores import DistanceStrategy

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH", "document.pdf")
COLLECTION = os.getenv("PG_VECTOR_COLLECTION_NAME", "minha_colecao")
DB_URL = os.getenv("DATABASE_URL")

def main():
    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(f"PDF não encontrado: {PDF_PATH}")

    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))

    PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION,
        connection=DB_URL,
        distance_strategy=DistanceStrategy.COSINE,
        use_jsonb=True
    )
    print(f"Ingestão concluída: {len(chunks)} chunks inseridos em '{COLLECTION}'.")

if __name__ == "__main__":
    main()
