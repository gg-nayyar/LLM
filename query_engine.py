import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import datetime

os.environ["API_KEY"] = "AIzaSyDG5tTiF6-1n1dHL7MB5P92uU3NCOcB3XY"
genai.configure(api_key=os.getenv("API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

model = genai.GenerativeModel("gemini-1.5-flash")

@app.post("/ask")
async def ask_query(query: QueryRequest):
    try:
        system_prompt = """
        You are an AI-powered **Legal Consultant** specialized in Indian law. 
        - You can't let your clients know about your AI identity.
        - Provide **accurate, concise, and well-structured legal advice**.
        - Break down complex legal terms in **simple, understandable language**.
        - If a law reference is required, mention **specific articles/sections**.
        - If a query is **out of scope**, politely say you **cannot provide advice**.
        - Do not generate fake legal citations; provide only factual answers.
        """

        user_query = f"{system_prompt}\n\nUser's Question: {query.question}"

        response = model.generate_content(user_query)
        full_text = response.text.strip()

        key_points = "\n- ".join(full_text.split(". ")[:3])

        structured_response = f"""\
**📝 Legal Advice:**  
{full_text}  

---

### 📌 **Key Takeaways:**  
- {key_points}  
- [Read Full Answer Above] 
        """

        return {
            "success": True,
            "answer": structured_response,
            "timestamp": datetime.datetime.now().isoformat(),
            "error": None,
        }
    except Exception as e:
        return {
            "success": False,
            "answer": None,
            "timestamp": datetime.datetime.now().isoformat(),
            "error": str(e),
        }