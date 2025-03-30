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


@app.get("/health", response_model=HealthCheck)
async def health():
    return {"status": "ok"}


@app.post("/generate", response_model=dict)
async def generate(prompt: Prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt.text}]
    )

    return {"response": response.choices[0].message.content}
