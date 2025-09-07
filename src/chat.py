
import os
from dotenv import load_dotenv
from search import search
from langchain_openai import ChatOpenAI

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def main():
    llm = ChatOpenAI(model=os.getenv("OPENAI_LLM","gpt-5-nano"), temperature=0)

    print("Faça sua pergunta (CTRL+C para sair):")
    while True:
        try:
            question = input("PERGUNTA: ").strip()
            if not question:
                continue

            results = search(question, k=10)
            if not results:
                print("RESPOSTA: Não tenho informações necessárias para responder sua pergunta.")
                continue

            contexto = "\n\n".join([d.page_content for d, _ in results])
            prompt = PROMPT_TEMPLATE.format(contexto=contexto, pergunta=question)

            ans = llm.invoke(prompt)
            text = ans.content if hasattr(ans, "content") else str(ans)

            if not text.strip():
                print("RESPOSTA: Não tenho informações necessárias para responder sua pergunta.")
            else:
                print(f"RESPOSTA: {text.strip()}")
        except KeyboardInterrupt:
            print("\nEncerrando.")
            break

if __name__ == "__main__":
    main()
