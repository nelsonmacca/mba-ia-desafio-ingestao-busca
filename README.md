
# Desafio MBA - Ingestão e Busca Semântica com LangChain + Postgres (pgvector)

Ajustado para uso com **drive D** no Windows.

## Estrutura
```
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── src/
│   ├── ingest.py
│   ├── search.py
│   ├── chat.py
├── document.pdf
└── README.md
```

## Passos de execução

1. **Criar .env**
   ```powershell
   copy .env.example .env
   notepad .env
   ```
   ➝ Coloque sua chave em `OPENAI_API_KEY`.

2. **Subir o banco**
   ```powershell
   docker compose up -d
   ```

3. **Criar ambiente Python**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Ingestão do PDF**
   Coloque seu arquivo em `document.pdf` na raiz e rode:
   ```powershell
   python src/ingest.py
   ```

5. **Chat (CLI)**
   ```powershell
   python src/chat.py
   ```
   ➝ Pergunte algo contido no PDF. Fora de contexto, a resposta será:
   `"Não tenho informações necessárias para responder sua pergunta."`
