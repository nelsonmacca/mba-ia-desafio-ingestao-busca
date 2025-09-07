import os, sys
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

COLLECTION = os.getenv("PG_VECTOR_COLLECTION_NAME", "minha_colecao")
DB_URL = os.getenv("DATABASE_URL")
EMBED_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

def search(query: str, k: int = 10):
    embeddings = OpenAIEmbeddings(model=EMBED_MODEL)

    vs = PGVector(
        embeddings=embeddings,            # <-- aqui é embeddings=
        collection_name=COLLECTION,
        connection=DB_URL
    )

    return vs.similarity_search_with_score(query, k=k)

if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "Qual o faturamento da Empresa SuperTechIABrazil?"
    results = search(q, k=10)
    for doc, score in results:
        print(f"[score={score:.4f}] (p.{doc.metadata.get('page','?')}) {doc.page_content[:200]}...")
