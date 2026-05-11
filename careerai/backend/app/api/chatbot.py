from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.api.auth import get_current_user

router = APIRouter()

RESPONSES = {
    "career": "Based on your profile, focus on Software Engineer or AI/ML Engineer. Both have strong market demand with 70%+ match potential.",
    "ats": "To improve ATS score: (1) Add dedicated Skills section (2) Quantify achievements with numbers (3) Use standard headers (4) Include keywords from job descriptions.",
    "skills": "Top skills in 2025: LangChain, Kubernetes, TypeScript, dbt, Rust. Prioritize based on your target role.",
    "salary": "Average tech salaries: SWE $112K, ML Engineer $135K, Cloud $118K, Data Analyst $88K. Remote roles often pay 10-20% more.",
    "interview": "For tech interviews: practice LeetCode daily, review system design basics, prepare STAR stories for behavioral questions.",
    "default": "I'm your AI Career Assistant. I can help with career recommendations, skill gaps, interview prep, and salary negotiation. What would you like to explore?",
}

class ChatMessage(BaseModel):
    message: str
    context: dict = {}

@router.post("/message")
async def chat(msg: ChatMessage, user=Depends(get_current_user)):
    lower = msg.message.lower()
    if any(w in lower for w in ["career","match","job","role"]):
        reply = RESPONSES["career"]
    elif any(w in lower for w in ["ats","score","improve","resume"]):
        reply = RESPONSES["ats"]
    elif any(w in lower for w in ["skill","learn","course"]):
        reply = RESPONSES["skills"]
    elif any(w in lower for w in ["salary","pay","compensation","earn"]):
        reply = RESPONSES["salary"]
    elif any(w in lower for w in ["interview","question","prepare"]):
        reply = RESPONSES["interview"]
    else:
        reply = RESPONSES["default"]
    return {"reply": reply, "user": user.get("full_name", "User")}
