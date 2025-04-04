from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from fastapi import UploadFile, File
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
import logging
import os
import tempfile

load_dotenv()
app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
vectorstore = Chroma.from_documents(pages, embeddings, persist_directory="./chroma_db")


class HealthCheck(BaseModel):
    status: str


class Prompt(BaseModel):
    text: str


class Response(BaseModel):
    response: str


@app.get("/health", response_model=HealthCheck)
async def health():
    return {"status": "ok"}


@app.post("/generate", response_model=Response)
async def generate(prompt: Prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt.text}]
        )

        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"error": f"OpenAI API failed: {str(e)}"}


@app.post("/upload", response_model=Response)
async def upload(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(await file.read())
            temp_path = temp_file.name

        loader = PyPDFLoader(temp_path)
        pages = [page async for page in loader.alazy_load()]
        logging.info(f"{pages[0].metadata}\n")
        logging.info(pages[0].page_content)

        if not file.filename.endswith(".pdf"):
            return {"error": "File must be a PDF"}

        return {"response": f"Loaded {len(pages)} pages"}
    except Exception as e:
        return {"error": f"Cannot process PDF: {str(e)}"}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
