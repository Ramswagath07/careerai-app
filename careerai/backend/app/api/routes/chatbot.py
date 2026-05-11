from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.security import get_current_user
from app.core.database import get_db

router = APIRouter()

class ChatMessage(BaseModel):
    message: str
    context: dict = {}

CAREER_KNOWLEDGE = {
    "salary": "Salaries vary by role and location. Software Engineers earn $85K–$140K, AI/ML Engineers $110–$165K, Cloud Engineers $95–$145K in the US. India salaries are 30–60% of US rates but growing rapidly.",
    "interview": "For tech interviews: 1) Practice LeetCode (medium-hard), 2) Study system design (Grokking the System Design), 3) Prepare behavioral questions using STAR method, 4) Know your resume cold, 5) Research the company's tech stack.",
    "resume": "ATS tips: Use keywords from job descriptions, add measurable achievements, include a skills section, use standard headings, keep to 1-2 pages, use clean formatting without tables/graphics that confuse parsers.",
    "career_change": "Transitioning to tech: 1) Choose a specific role, 2) Build 3-5 portfolio projects, 3) Get 1-2 certifications, 4) Network on LinkedIn, 5) Apply to startups first, 6) Consider bootcamps for fast-tracking.",
    "skills": "Top skills for 2025: Python (universal), TypeScript (web), Kubernetes (infra), LangChain/RAG (AI), dbt (data), Terraform (cloud), React (frontend). Focus on 2-3 deep skills rather than many shallow ones.",
    "default": "I'm your AI Career Assistant! I can help with: career path advice, ATS score improvement, skill gap analysis, interview preparation, salary negotiation, and learning roadmaps. What specific area would you like to explore?",
}

@router.post("/message")
async def chat(msg: ChatMessage, current_user=Depends(get_current_user)):
    text = msg.message.lower()
    
    reply = CAREER_KNOWLEDGE["default"]
    if any(w in text for w in ["salary","pay","earn","compensation","money"]):
        reply = CAREER_KNOWLEDGE["salary"]
    elif any(w in text for w in ["interview","prep","practice","leetcode"]):
        reply = CAREER_KNOWLEDGE["interview"]
    elif any(w in text for w in ["resume","ats","cv","format"]):
        reply = CAREER_KNOWLEDGE["resume"]
    elif any(w in text for w in ["switch","change","transition","new career"]):
        reply = CAREER_KNOWLEDGE["career_change"]
    elif any(w in text for w in ["skill","learn","course","study"]):
        reply = CAREER_KNOWLEDGE["skills"]
    
    # Save to history
    db = get_db()
    await db.chat_history.insert_one({
        "user_id": str(current_user["_id"]),
        "user_message": msg.message,
        "bot_reply": reply,
    })
    
    return {"reply": reply, "suggestions": ["Tell me about salary negotiation", "What skills should I learn?", "How to ace interviews?"]}

@router.get("/history")
async def chat_history(current_user=Depends(get_current_user)):
    db = get_db()
    history = await db.chat_history.find(
        {"user_id": str(current_user["_id"])},
        {"user_message":1,"bot_reply":1,"_id":0}
    ).sort("_id",-1).limit(50).to_list(50)
    return history[::-1]
