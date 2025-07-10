from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import openai
import os

app = FastAPI()

# ✅ ALLOW YOUR WORDPRESS DOMAIN TO ACCESS THIS BACKEND
origins = ["https://aiaffiliatecommission.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # allow POST
    allow_headers=["*"],
)

# ✅ Load your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Input format
class TitleRequest(BaseModel):
    text: str

# Output format
class TitleResponse(BaseModel):
    titles: List[str]

# Your AI-powered endpoint
@app.post("/generate", response_model=TitleResponse)
async def generate_titles(request: TitleRequest):
    prompt = (
        f"Give me 5 catchy blog post titles for this topic:\n\n"
        f"Topic: {request.text}\n\n"
        f"Titles:"
    )

    response = openai.Completion.create(
        engine="text-davinci-003",  # or use gpt-3.5-turbo if using ChatCompletion
        prompt=prompt,
        max_tokens=100,
        temperature=0.7,
        n=1,
        stop=None,
    )

    titles_raw = response.choices[0].text.strip().split("\n")
    titles_clean = [t.strip("0123456789. ").strip() for t in titles_raw if t.strip()]

    return {"titles": titles_clean}
