from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.core.database import get_db
from app.ml.resume_analyzer import CAREER_PROFILES, match_careers

router = APIRouter()

LEARNING_ROADMAPS = {
    "Software Engineer": [
        {"step": 1, "title": "Core Programming", "desc": "Master Python/JS, OOP, algorithms", "months": 2, "status": "recommended"},
        {"step": 2, "title": "Web Frameworks", "desc": "React frontend, FastAPI/Django backend", "months": 2, "status": "recommended"},
        {"step": 3, "title": "Databases", "desc": "SQL, MongoDB, Redis basics", "months": 1, "status": "recommended"},
        {"step": 4, "title": "Cloud & DevOps", "desc": "AWS, Docker, CI/CD pipelines", "months": 2, "status": "advanced"},
        {"step": 5, "title": "System Design", "desc": "Scalable systems, microservices, caching", "months": 2, "status": "advanced"},
    ],
    "AI/ML Engineer": [
        {"step": 1, "title": "Python & Math", "desc": "Python, linear algebra, statistics", "months": 2, "status": "recommended"},
        {"step": 2, "title": "ML Fundamentals", "desc": "Scikit-learn, supervised/unsupervised learning", "months": 2, "status": "recommended"},
        {"step": 3, "title": "Deep Learning", "desc": "TensorFlow/PyTorch, CNNs, RNNs, Transformers", "months": 3, "status": "recommended"},
        {"step": 4, "title": "MLOps", "desc": "Model deployment, monitoring, Docker, cloud ML", "months": 2, "status": "advanced"},
        {"step": 5, "title": "LLMs & GenAI", "desc": "LangChain, RAG, fine-tuning, prompt engineering", "months": 2, "status": "advanced"},
    ],
}

COURSES_DB = [
    {"title": "Python for Everybody", "platform": "Coursera", "url": "https://coursera.org/learn/python", "rating": 4.8, "duration": "16h", "free": True, "skills": ["Python"]},
    {"title": "The Complete React Developer Course", "platform": "Udemy", "url": "https://udemy.com", "rating": 4.9, "duration": "40h", "free": False, "price": "$14.99", "skills": ["React","JavaScript"]},
    {"title": "AWS Certified Solutions Architect", "platform": "Coursera", "url": "https://coursera.org", "rating": 4.7, "duration": "30h", "free": True, "skills": ["AWS","Cloud"]},
    {"title": "Machine Learning Specialization", "platform": "Coursera", "url": "https://coursera.org/specializations/machine-learning-introduction", "rating": 4.9, "duration": "60h", "free": True, "skills": ["Machine Learning","Python"]},
    {"title": "Docker & Kubernetes Bootcamp", "platform": "Udemy", "url": "https://udemy.com", "rating": 4.7, "duration": "22h", "free": False, "price": "$13.99", "skills": ["Docker","Kubernetes"]},
    {"title": "SQL for Data Analysis", "platform": "Udacity", "url": "https://udacity.com", "rating": 4.6, "duration": "12h", "free": True, "skills": ["SQL"]},
    {"title": "Deep Learning Specialization", "platform": "Coursera", "url": "https://coursera.org/specializations/deep-learning", "rating": 4.9, "duration": "64h", "free": True, "skills": ["Deep Learning","TensorFlow"]},
    {"title": "Figma UI/UX Design Essentials", "platform": "Udemy", "url": "https://udemy.com", "rating": 4.8, "duration": "14h", "free": False, "price": "$12.99", "skills": ["Figma"]},
    {"title": "Cybersecurity Fundamentals", "platform": "edX", "url": "https://edx.org", "rating": 4.6, "duration": "18h", "free": True, "skills": ["Cybersecurity","Linux"]},
    {"title": "LangChain for LLM Apps", "platform": "DeepLearning.AI", "url": "https://deeplearning.ai", "rating": 4.8, "duration": "8h", "free": True, "skills": ["LLM","Python"]},
]

@router.get("/")
async def get_careers():
    return [{"title": k, **{kk: vv for kk, vv in v.items() if kk != "skills"}, "key_skills": v["skills"][:5]}
            for k, v in CAREER_PROFILES.items()]

@router.get("/{career_title}/roadmap")
async def get_roadmap(career_title: str, current_user=Depends(get_current_user)):
    steps = LEARNING_ROADMAPS.get(career_title, LEARNING_ROADMAPS["Software Engineer"])
    return {"career": career_title, "steps": steps, "total_months": sum(s["months"] for s in steps)}

@router.get("/courses/recommended")
async def get_courses(skill: str = None):
    if skill:
        filtered = [c for c in COURSES_DB if any(skill.lower() in s.lower() for s in c["skills"])]
        return filtered or COURSES_DB[:6]
    return COURSES_DB

@router.post("/match")
async def match_from_skills(skills: list[str]):
    return match_careers(skills)
