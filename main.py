from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class HealthCheck(BaseModel):
    status: str


class Prompt(BaseModel):
    text: str


class Response(BaseModel):
    rsponse: str


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
