"""
CareerAI — Career Recommendation Engine
Uses cosine similarity + skill matching to rank career paths.
"""

import math
from typing import List, Dict

CAREERS_DB = [
    {
        "title": "Software Engineer",
        "icon": "💻",
        "description": "Design and develop scalable software systems, APIs, and applications.",
        "required_skills": ["Python","JavaScript","React","Node.js","SQL","Git","REST API","Docker","Agile"],
        "salary_range": "$85K–$140K",
        "demand_level": "Very High",
        "growth_rate": "+25% (2024-2030)",
        "categories": ["tech","development"],
    },
    {
        "title": "Data Analyst",
        "icon": "📊",
        "description": "Transform raw data into actionable business insights using analytics tools.",
        "required_skills": ["Python","SQL","Pandas","Excel","Data Analysis","Agile","PostgreSQL","Tableau"],
        "salary_range": "$65K–$105K",
        "demand_level": "High",
        "growth_rate": "+23% (2024-2030)",
        "categories": ["data","analytics"],
    },
    {
        "title": "AI/ML Engineer",
        "icon": "🤖",
        "description": "Build and deploy machine learning models and AI-powered systems.",
        "required_skills": ["Python","Machine Learning","TensorFlow","PyTorch","scikit-learn","NLP","Pandas","NumPy","Docker"],
        "salary_range": "$110K–$175K",
        "demand_level": "Very High",
        "growth_rate": "+40% (2024-2030)",
        "categories": ["ai","ml","data"],
    },
    {
        "title": "Cloud Engineer",
        "icon": "☁️",
        "description": "Architect and manage cloud infrastructure at enterprise scale.",
        "required_skills": ["AWS","Docker","Kubernetes","Terraform","Linux","CI/CD","Python","Git"],
        "salary_range": "$100K–$155K",
        "demand_level": "High",
        "growth_rate": "+28% (2024-2030)",
        "categories": ["cloud","devops"],
    },
    {
        "title": "UI/UX Designer",
        "icon": "🎨",
        "description": "Craft beautiful, user-centered digital experiences and interfaces.",
        "required_skills": ["Figma","Adobe XD","HTML/CSS","JavaScript","React","User Research"],
        "salary_range": "$70K–$115K",
        "demand_level": "Medium",
        "growth_rate": "+13% (2024-2030)",
        "categories": ["design"],
    },
    {
        "title": "Cybersecurity Analyst",
        "icon": "🛡️",
        "description": "Protect systems and data from threats through monitoring and incident response.",
        "required_skills": ["Linux","Python","SQL","Agile","Docker","CI/CD"],
        "salary_range": "$80K–$130K",
        "demand_level": "High",
        "growth_rate": "+35% (2024-2030)",
        "categories": ["security"],
    },
    {
        "title": "DevOps Engineer",
        "icon": "⚙️",
        "description": "Bridge development and operations to accelerate delivery pipelines.",
        "required_skills": ["Docker","Kubernetes","CI/CD","Linux","Python","AWS","Git","Terraform"],
        "salary_range": "$95K–$145K",
        "demand_level": "Very High",
        "growth_rate": "+22% (2024-2030)",
        "categories": ["devops","cloud"],
    },
    {
        "title": "Data Engineer",
        "icon": "🔧",
        "description": "Build data pipelines and infrastructure to power analytics platforms.",
        "required_skills": ["Python","SQL","Spark","Kafka","AWS","Docker","PostgreSQL","MongoDB"],
        "salary_range": "$90K–$145K",
        "demand_level": "High",
        "growth_rate": "+30% (2024-2030)",
        "categories": ["data","engineering"],
    },
    {
        "title": "Full Stack Developer",
        "icon": "🌐",
        "description": "Build end-to-end web applications from database to UI.",
        "required_skills": ["JavaScript","TypeScript","React","Node.js","SQL","MongoDB","REST API","Git","Docker"],
        "salary_range": "$80K–$135K",
        "demand_level": "Very High",
        "growth_rate": "+20% (2024-2030)",
        "categories": ["tech","development"],
    },
    {
        "title": "Product Manager",
        "icon": "📋",
        "description": "Define product vision, roadmap, and work cross-functionally to ship great products.",
        "required_skills": ["Agile","SQL","Data Analysis","Excel"],
        "salary_range": "$95K–$160K",
        "demand_level": "High",
        "growth_rate": "+10% (2024-2030)",
        "categories": ["product","management"],
    },
]

def _cosine_similarity(vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
    keys = set(vec_a) | set(vec_b)
    dot = sum(vec_a.get(k, 0) * vec_b.get(k, 0) for k in keys)
    mag_a = math.sqrt(sum(v**2 for v in vec_a.values()))
    mag_b = math.sqrt(sum(v**2 for v in vec_b.values()))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)

def recommend_careers(detected_skills: List[str], top_n: int = 6) -> List[Dict]:
    """
    Match detected skills against career profiles using cosine similarity.
    Returns top_n matches sorted by score descending.
    """
    detected_set = set(s.lower() for s in detected_skills)
    user_vec = {s.lower(): 1.0 for s in detected_skills}

    results = []
    for career in CAREERS_DB:
        req = career["required_skills"]
        career_vec = {s.lower(): 1.0 for s in req}

        similarity = _cosine_similarity(user_vec, career_vec)
        matching = [s for s in req if s.lower() in detected_set]
        missing  = [s for s in req if s.lower() not in detected_set]

        # Score: cosine sim (0-1) mapped to 40-99 range + skill overlap bonus
        overlap_ratio = len(matching) / max(len(req), 1)
        raw_score = (similarity * 0.5 + overlap_ratio * 0.5) * 100
        final_score = round(min(99, max(40, raw_score + 10)), 1)

        results.append({
            "title": career["title"],
            "icon": career.get("icon", "💼"),
            "match_score": final_score,
            "salary_range": career["salary_range"],
            "demand_level": career["demand_level"],
            "required_skills": req,
            "matching_skills": matching,
            "missing_skills": missing[:5],
            "description": career["description"],
            "growth_rate": career["growth_rate"],
        })

    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results[:top_n]
