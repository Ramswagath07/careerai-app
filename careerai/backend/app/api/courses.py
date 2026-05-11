from fastapi import APIRouter

router = APIRouter()

COURSES = [
    {"id":"c1","name":"Python for Data Science & ML","platform":"Udemy","rating":4.8,"duration":"22h","price":"$14.99","level":"Beginner","skills":["Python","Pandas","NumPy","scikit-learn"],"url":"https://udemy.com"},
    {"id":"c2","name":"AWS Certified Solutions Architect","platform":"Coursera","rating":4.7,"duration":"35h","price":"Free Audit","level":"Intermediate","skills":["AWS","Cloud","Architecture"],"url":"https://coursera.org"},
    {"id":"c3","name":"React — The Complete Guide 2025","platform":"Udemy","rating":4.9,"duration":"48h","price":"$19.99","level":"All Levels","skills":["React","JavaScript","TypeScript"],"url":"https://udemy.com"},
    {"id":"c4","name":"Deep Learning Specialization","platform":"Coursera","rating":4.9,"duration":"64h","price":"Free Audit","level":"Advanced","skills":["Deep Learning","TensorFlow","ML"],"url":"https://coursera.org"},
    {"id":"c5","name":"Docker & Kubernetes Bootcamp","platform":"Udemy","rating":4.7,"duration":"24h","price":"$13.99","level":"Intermediate","skills":["Docker","Kubernetes","DevOps"],"url":"https://udemy.com"},
    {"id":"c6","name":"Introduction to Cybersecurity","platform":"edX","rating":4.6,"duration":"20h","price":"Free","level":"Beginner","skills":["Security","Networking","Linux"],"url":"https://edx.org"},
    {"id":"c7","name":"LangChain & Vector Databases in Production","platform":"Udemy","rating":4.8,"duration":"16h","price":"$12.99","level":"Advanced","skills":["LangChain","LLMs","Python"],"url":"https://udemy.com"},
    {"id":"c8","name":"PostgreSQL Bootcamp","platform":"Udemy","rating":4.7,"duration":"18h","price":"$11.99","level":"Beginner","skills":["SQL","PostgreSQL","Databases"],"url":"https://udemy.com"},
]

@router.get("/")
async def list_courses(skill: str = ""):
    if skill:
        return [c for c in COURSES if any(skill.lower() in s.lower() for s in c["skills"])]
    return COURSES
