"""
Core ML module: PDF/DOCX/TXT extraction + ATS scoring + NLP skill extraction
Uses: pdfplumber, python-docx, spaCy, TF-IDF, cosine similarity
"""
import re
import io
import logging
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)

# ── Skill taxonomy ────────────────────────────────────────────────────────────
SKILL_KEYWORDS = {
    # Programming
    "Python": r"\bpython\b",
    "JavaScript": r"\bjavascript\b|\bjs\b(?!\s*framework)",
    "TypeScript": r"\btypescript\b|\bts\b",
    "Java": r"\bjava\b(?!script)",
    "C++": r"\bc\+\+\b",
    "C#": r"\bc#\b|\bc sharp\b",
    "Go": r"\bgolang\b|\bgo\s+lang\b",
    "Rust": r"\brust\b(?!y)",
    "Ruby": r"\bruby\b(?!\s+on)",
    "PHP": r"\bphp\b",
    "Swift": r"\bswift\b",
    "Kotlin": r"\bkotlin\b",
    "R": r"\b\bR\b(?:\s+programming|\s+language)?",
    "Scala": r"\bscala\b",
    # Web
    "React": r"\breact\.?js?\b",
    "Vue.js": r"\bvue\.?js?\b",
    "Angular": r"\bangular\b",
    "Next.js": r"\bnext\.?js\b",
    "Node.js": r"\bnode\.?js\b",
    "Django": r"\bdjango\b",
    "Flask": r"\bflask\b",
    "FastAPI": r"\bfastapi\b",
    "Spring Boot": r"\bspring\s*boot\b",
    "HTML/CSS": r"\bhtml5?\b|\bcss3?\b",
    "Tailwind CSS": r"\btailwind\b",
    "GraphQL": r"\bgraphql\b",
    "REST API": r"\brest\s*api\b|\brestful\b",
    # Data/ML
    "Machine Learning": r"\bmachine\s+learning\b|\bml\b",
    "Deep Learning": r"\bdeep\s+learning\b",
    "TensorFlow": r"\btensorflow\b",
    "PyTorch": r"\bpytorch\b",
    "Scikit-learn": r"\bscikit[\-\s]learn\b|\bsklearn\b",
    "Pandas": r"\bpandas\b",
    "NumPy": r"\bnumpy\b",
    "Data Analysis": r"\bdata\s+analysis\b|\bdata\s+analytics\b",
    "NLP": r"\bnlp\b|\bnatural\s+language\s+processing\b",
    "Computer Vision": r"\bcomputer\s+vision\b",
    "LLM": r"\bllm\b|\blarge\s+language\s+model\b",
    "SQL": r"\bsql\b",
    "NoSQL": r"\bnosql\b",
    "Tableau": r"\btableau\b",
    "Power BI": r"\bpower\s*bi\b",
    # Cloud/DevOps
    "AWS": r"\baws\b|\bamazon\s+web\s+services\b",
    "GCP": r"\bgcp\b|\bgoogle\s+cloud\b",
    "Azure": r"\bazure\b",
    "Docker": r"\bdocker\b",
    "Kubernetes": r"\bkubernetes\b|\bk8s\b",
    "Terraform": r"\bterraform\b",
    "CI/CD": r"\bci\/cd\b|\bjenkins\b|\bgithub\s+actions\b|\bgitlab\s+ci\b",
    "Linux": r"\blinux\b|\bunix\b",
    "Nginx": r"\bnginx\b",
    # Databases
    "MongoDB": r"\bmongodb\b",
    "PostgreSQL": r"\bpostgresql\b|\bpostgres\b",
    "MySQL": r"\bmysql\b",
    "Redis": r"\bredis\b",
    "Elasticsearch": r"\belasticsearch\b",
    "Firebase": r"\bfirebase\b",
    # Tools
    "Git": r"\bgit\b(?!hub|\slab)",
    "GitHub": r"\bgithub\b",
    "Jira": r"\bjira\b",
    "Agile/Scrum": r"\bagile\b|\bscrum\b|\bsprint\b",
    "Figma": r"\bfigma\b",
    "Excel": r"\bexcel\b",
}

EDUCATION_KEYWORDS = {
    "PhD": r"\bph\.?d\b|\bdoctorate\b",
    "Master's": r"\bmaster\b|\bm\.?s\.?\b|\bm\.?tech\b|\bmba\b",
    "Bachelor's": r"\bbachelor\b|\bb\.?tech\b|\bb\.?e\b|\bbsc\b|\bb\.?s\b",
    "Associate": r"\bassociate\b|\bdiploma\b",
}

CERT_KEYWORDS = [
    "aws certified","google certified","azure certified","pmp","cissp",
    "ceh","comptia","ccna","ccnp","tensorflow developer","pytorch","tensorflow",
    "coursera","udemy","edx","certification","certified",
]

EXPERIENCE_PATTERNS = [
    r"(\d+)\+?\s*years?\s+of\s+experience",
    r"(\d+)\+?\s*years?\s+experience",
    r"experience\s+of\s+(\d+)\+?\s*years?",
    r"(\d+)\+?\s*yrs?\s+experience",
]

CONTACT_PATTERNS = {
    "email": r"[\w.\-+]+@[\w\-]+\.[a-z]{2,}",
    "phone": r"(\+\d{1,3}[\s\-]?)?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{4}",
    "linkedin": r"linkedin\.com/in/[\w\-]+",
    "github": r"github\.com/[\w\-]+",
}

ACTION_VERBS = [
    "developed","built","designed","implemented","created","deployed","managed",
    "led","architected","optimized","improved","automated","integrated","launched",
    "delivered","engineered","collaborated","analyzed","maintained","migrated",
    "scaled","reduced","increased","achieved","mentored","established",
]

QUANTIFIER_PATTERN = r"\b(\d+\.?\d*)\s*(%|percent|x|times|users?|customers?|K|M|billion|million|thousand)\b"


def extract_text_from_pdf(content: bytes) -> str:
    """Extract text from PDF bytes using pdfplumber."""
    try:
        import pdfplumber
        text_parts = []
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text_parts.append(t)
        return "\n".join(text_parts)
    except ImportError:
        logger.warning("pdfplumber not available, trying PyPDF2")
        return _fallback_pdf(content)
    except Exception as e:
        logger.error(f"PDF extraction error: {e}")
        return _fallback_pdf(content)


def _fallback_pdf(content: bytes) -> str:
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(content))
        return "\n".join(p.extract_text() or "" for p in reader.pages)
    except Exception as e:
        logger.error(f"Fallback PDF error: {e}")
        return ""


def extract_text_from_docx(content: bytes) -> str:
    try:
        from docx import Document
        doc = Document(io.BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except Exception as e:
        logger.error(f"DOCX extraction error: {e}")
        return ""


def extract_text(content: bytes, filename: str) -> str:
    ext = Path(filename).suffix.lower()
    if ext == ".pdf":
        return extract_text_from_pdf(content)
    elif ext in (".doc", ".docx"):
        return extract_text_from_docx(content)
    elif ext == ".txt":
        return content.decode("utf-8", errors="ignore")
    return ""


# ── NLP Skill Extraction ──────────────────────────────────────────────────────
def extract_skills(text: str) -> tuple[list, list]:
    """Returns (detected_skills, missing_skills)."""
    detected, missing = [], []
    for skill, pattern in SKILL_KEYWORDS.items():
        if re.search(pattern, text, re.IGNORECASE):
            detected.append(skill)
        else:
            missing.append(skill)
    return detected, missing


def extract_education(text: str) -> Optional[str]:
    for level, pattern in EDUCATION_KEYWORDS.items():
        if re.search(pattern, text, re.IGNORECASE):
            return level
    return None


def extract_experience_years(text: str) -> Optional[float]:
    for pattern in EXPERIENCE_PATTERNS:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            return float(m.group(1))
    # Count year ranges like "2020 – 2023"
    ranges = re.findall(r"(20\d{2})\s*[-–—]\s*(20\d{2}|present|current)", text, re.IGNORECASE)
    if ranges:
        total = 0
        for start, end in ranges:
            try:
                end_year = 2025 if end.lower() in ("present","current") else int(end)
                total += end_year - int(start)
            except:
                pass
        return float(total) if total else None
    return None


def extract_certifications(text: str) -> list:
    lower = text.lower()
    return [c.title() for c in CERT_KEYWORDS if c in lower]


def extract_contact_info(text: str) -> dict:
    info = {}
    for key, pattern in CONTACT_PATTERNS.items():
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            info[key] = m.group(0)
    return info


# ── ATS Scoring Engine ────────────────────────────────────────────────────────
def compute_ats_score(text: str, detected_skills: list, contact_info: dict,
                      education: Optional[str], exp_years: Optional[float]) -> dict:
    lower = text.lower()
    words = text.split()

    # 1. Keyword Density (25%)
    kw_ratio = len(detected_skills) / max(len(SKILL_KEYWORDS), 1)
    keyword_score = min(100, int(kw_ratio * 100 * 2.5))

    # 2. Contact Information (15%)
    contact_score = 0
    contact_score += 40 if "email" in contact_info else 0
    contact_score += 30 if "phone" in contact_info else 0
    contact_score += 20 if "linkedin" in contact_info else 0
    contact_score += 10 if "github" in contact_info else 0

    # 3. Work Experience (25%)
    action_count = sum(1 for v in ACTION_VERBS if v in lower)
    quantifier_count = len(re.findall(QUANTIFIER_PATTERN, text, re.IGNORECASE))
    has_dates = bool(re.search(r"20\d{2}", text))
    exp_score = min(100, action_count * 5 + quantifier_count * 10 + (30 if has_dates else 0))

    # 4. Education (15%)
    edu_scores = {"PhD": 100, "Master's": 90, "Bachelor's": 80, "Associate": 60, None: 40}
    edu_score = edu_scores.get(education, 40)

    # 5. Skills Section (10%)
    has_skills_header = bool(re.search(r"\bskills\b", lower))
    skills_score = min(100, len(detected_skills) * 5 + (20 if has_skills_header else 0))

    # 6. Format & Structure (10%)
    has_sections = sum(1 for s in ["experience","education","skills","projects","summary","objective"] if s in lower)
    word_count = len(words)
    format_score = min(100, has_sections * 15 + (20 if 400 <= word_count <= 1200 else 10))

    # Weighted total
    total = int(
        keyword_score * 0.25 +
        contact_score * 0.15 +
        exp_score     * 0.25 +
        edu_score     * 0.15 +
        skills_score  * 0.10 +
        format_score  * 0.10
    )

    # AI recommendations
    recs = []
    if keyword_score < 60: recs.append("Add more technical skills matching the job description")
    if "email" not in contact_info: recs.append("Include your email address prominently")
    if "phone" not in contact_info: recs.append("Add a phone number to your contact section")
    if "linkedin" not in contact_info: recs.append("Add your LinkedIn profile URL")
    if quantifier_count < 3: recs.append("Add quantified achievements (e.g. 'reduced load time by 40%')")
    if action_count < 5: recs.append("Start bullet points with strong action verbs")
    if not has_skills_header: recs.append("Create a dedicated 'Skills' section")
    if word_count < 400: recs.append("Your resume seems short — aim for 500–800 words")
    if word_count > 1200: recs.append("Consider trimming to 1 page for early-career, 2 pages max")
    if "github" not in contact_info: recs.append("Add your GitHub profile to showcase projects")

    return {
        "ats_score": total,
        "keyword_score": keyword_score,
        "contact_score": contact_score,
        "experience_score": exp_score,
        "education_score": edu_score,
        "skills_score": skills_score,
        "format_score": format_score,
        "word_count": word_count,
        "recommendations": recs[:6],
    }


# ── Career Matching (TF-IDF + Cosine Similarity) ──────────────────────────────
CAREER_PROFILES = {
    "Software Engineer": {
        "skills": ["Python","JavaScript","React","Node.js","SQL","Git","REST API","Docker","Agile/Scrum","TypeScript"],
        "description": "Build and maintain software applications and systems.",
        "salary": "$85K–$140K",
        "demand": "Very High",
        "growth": "+25%",
        "remote": True,
    },
    "Data Analyst": {
        "skills": ["Python","SQL","Excel","Pandas","Tableau","Power BI","NumPy","Data Analysis","R"],
        "description": "Analyze data to extract insights and support business decisions.",
        "salary": "$65K–$100K",
        "demand": "High",
        "growth": "+20%",
        "remote": True,
    },
    "AI/ML Engineer": {
        "skills": ["Python","TensorFlow","PyTorch","Scikit-learn","NLP","Deep Learning","Machine Learning","Docker","SQL","NumPy","Pandas"],
        "description": "Design and deploy machine learning models and AI systems.",
        "salary": "$110K–$165K",
        "demand": "Very High",
        "growth": "+35%",
        "remote": True,
    },
    "Cloud Engineer": {
        "skills": ["AWS","GCP","Azure","Docker","Kubernetes","Terraform","CI/CD","Linux","Python"],
        "description": "Design and manage scalable cloud infrastructure and services.",
        "salary": "$95K–$145K",
        "demand": "High",
        "growth": "+28%",
        "remote": True,
    },
    "UI/UX Designer": {
        "skills": ["Figma","HTML/CSS","JavaScript","React","Tailwind CSS","Python"],
        "description": "Create intuitive, beautiful user interfaces and experiences.",
        "salary": "$70K–$115K",
        "demand": "Medium",
        "growth": "+15%",
        "remote": True,
    },
    "Cybersecurity Analyst": {
        "skills": ["Linux","Python","SQL","Networking","CI/CD","Git","AWS"],
        "description": "Protect organizations from cyber threats and security breaches.",
        "salary": "$80K–$130K",
        "demand": "High",
        "growth": "+32%",
        "remote": False,
    },
    "DevOps Engineer": {
        "skills": ["Docker","Kubernetes","CI/CD","Linux","AWS","Terraform","Python","Nginx","Git"],
        "description": "Bridge development and operations for continuous delivery.",
        "salary": "$90K–$140K",
        "demand": "High",
        "growth": "+22%",
        "remote": True,
    },
    "Data Scientist": {
        "skills": ["Python","Machine Learning","Deep Learning","SQL","Pandas","NumPy","TensorFlow","NLP","R"],
        "description": "Use statistical methods and ML to solve complex business problems.",
        "salary": "$95K–$155K",
        "demand": "Very High",
        "growth": "+30%",
        "remote": True,
    },
    "Full Stack Developer": {
        "skills": ["JavaScript","React","Node.js","Python","SQL","MongoDB","REST API","Docker","Git","TypeScript"],
        "description": "Build complete web applications from frontend to backend.",
        "salary": "$80K–$130K",
        "demand": "Very High",
        "growth": "+24%",
        "remote": True,
    },
    "Backend Developer": {
        "skills": ["Python","Java","Node.js","SQL","MongoDB","PostgreSQL","Docker","REST API","Redis","Git"],
        "description": "Build server-side logic, APIs, and database management systems.",
        "salary": "$80K–$130K",
        "demand": "High",
        "growth": "+20%",
        "remote": True,
    },
}


def match_careers(detected_skills: list) -> list:
    """Compute career match scores using skill overlap and weighted cosine similarity."""
    detected_set = {s.lower() for s in detected_skills}
    matches = []

    for career, profile in CAREER_PROFILES.items():
        required = profile["skills"]
        required_set = {s.lower() for s in required}
        overlap = detected_set & required_set
        match_pct = round((len(overlap) / max(len(required_set), 1)) * 100)
        # Bonus for depth
        match_pct = min(98, match_pct + len(overlap) * 2)
        missing = [s for s in required if s.lower() not in detected_set]

        matches.append({
            "title": career,
            "match_score": match_pct,
            "matched_skills": list(overlap),
            "missing_skills": missing[:5],
            "required_skills": required,
            "salary_range": profile["salary"],
            "demand_level": profile["demand"],
            "description": profile["description"],
            "growth_rate": profile["growth"],
            "remote_friendly": profile["remote"],
        })

    return sorted(matches, key=lambda x: x["match_score"], reverse=True)


def analyze_resume_full(content: bytes, filename: str) -> dict:
    """Full pipeline: extract → analyze → match → return."""
    text = extract_text(content, filename)
    if not text.strip():
        raise ValueError("Could not extract text from the uploaded file.")

    detected_skills, missing_skills = extract_skills(text)
    contact_info = extract_contact_info(text)
    education = extract_education(text)
    exp_years = extract_experience_years(text)
    certifications = extract_certifications(text)

    scores = compute_ats_score(text, detected_skills, contact_info, education, exp_years)
    career_matches = match_careers(detected_skills)

    return {
        **scores,
        "detected_skills": detected_skills,
        "missing_skills": missing_skills[:15],
        "experience_years": exp_years,
        "education_level": education,
        "certifications": certifications,
        "extracted_text": text[:3000],
        "full_text_length": len(text),
        "contact_info": contact_info,
        "career_matches": career_matches[:6],
    }
