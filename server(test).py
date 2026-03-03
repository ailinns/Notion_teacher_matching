import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai

from mcp_tools import MCPToolRegistry

load_dotenv()
# ใส่ Google API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# เลือก model
model = genai.GenerativeModel("gemini-1.5-pro")

# -----------------------
# FastAPI Setup
# -----------------------
app = FastAPI()
mcp = MCPToolRegistry()


# -----------------------
# Request Model
# -----------------------
class TopicRequest(BaseModel):
    topic: str


# -----------------------
# Keyword Extraction
# -----------------------
def extract_keywords(topic: str):

    prompt = f"""
    Extract important technical keywords from this thesis topic.
    Return only a comma-separated list.

    Topic: {topic}
    """

    response = model.generate_content(prompt)

    text = response.text.strip()

    # แปลง string → list
    keywords = [k.strip() for k in text.split(",") if k.strip()]

    return keywords


# -----------------------
# API Endpoint
# -----------------------
@app.post("/api/match")
def match_topic(request: TopicRequest):

    topic = request.topic

    # 1️⃣ Extract keywords using Gemini
    keywords = extract_keywords(topic)

    # 2️⃣ Match with Excel ผ่าน MCP
    top3 = mcp.execute(
        "match_excel",
        {"keywords": keywords}
    )

    # 3️⃣ Save best result to Notion ผ่าน MCP
    if top3:
        mcp.execute(
        "save_log",
    {
        "topic": topic,
        "keywords": keywords,
        "top_advisors": top3
    }
)
    # 4️⃣ Return response to frontend
    return {
        "topic": topic,
        "keywords": keywords,
        "top_advisors": top3
    }