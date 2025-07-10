from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

# Init FastAPI
app = FastAPI()
origins = ["https://aiaffiliatecommission.com"]  # Frontend domain

# Allow all CORS (for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set your OpenAI key (we'll use Render's env vars later)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define input schema
class Topic(BaseModel):
    text: str

@app.post("/generate")
async def generate_titles(data: Topic):
    prompt = f"Generate 5 catchy blog post titles about: {data.text}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=100,
    )

    result = response.choices[0].message.content.strip()
    titles = result.split("\n")
    
    # Clean up titles
    cleaned = [title.strip("1234567890. ").strip() for title in titles if title.strip()]
    return {"titles": cleaned}
