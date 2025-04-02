# Document Q&A Bot

A FastAPI app for RAG-based document querying (in progress).

## Setup

1. Clone the repo: `git clone https://github.com/FelipeMejia/document-qa-bot`
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `uvicorn main:app --reload`

## Endpoints

- `GET /health`: Returns {"status": "ok"}
- `POST /generate`: Takes {"text": "your prompt"} and returns {"response": "generated text by chatGPT"}
- `POST /upload`: Loads a PDF and extracts its content (in progress)
