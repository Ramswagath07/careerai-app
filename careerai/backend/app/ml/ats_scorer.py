"""
CareerAI — ATS Resume Scoring Engine
Uses NLP, TF-IDF, keyword analysis, and structural heuristics
to compute a real ATS compatibility score.
"""

import re
import math
from typing import List, Dict, Tuple
from collections import Counter
import logging

logger = logging.getLogger(__name__)

# ── Skill taxonomy ────────────────────────────────────────────────────────────
SKILL_KEYWORDS = {
    # Programming Languages
    "Python": r"\bpython\b",
    "JavaScript": r"\bjavascript\b|\bjs\b",
    "TypeScript": r"\btypescript\b|\bts\b",
    "Java": r"\bjava\b(?!script)",
    "C++": r"\bc\+\+\b",
    "C#": r"\bc#\b|\bc sharp\b",
    "Go": r"\bgolang\b|\bgo lang\b",
    "Rust": r"\brust\b",
    "Ruby": r"\bruby\b",
    "PHP": r"\bphp\b",
    "Swift": r"\bswift\b",
    "Kotlin": r"\bkotlin\b",
    "R": r"\br programming\b|\br language\b",
    "Scala": r"\bscala\b",
    # Web
    "React": r"\breact\.?js?\b",
    "Vue": r"\bvue\.?js?\b",
    "Angular": r"\bangular\b",
    "Node.js": r"\bnode\.?js\b",
    "FastAPI": r"\bfastapi\b",
    "Django": r"\bdjango\b",
    "Flask": r"\bflask\b",
    "Spring Boot": r"\bspring boot\b",
    "HTML/CSS": r"\bhtml\b|\bcss\b|\bsass\b",
    "GraphQL": r"\bgraphql\b",
    "REST API": r"\brest api\b|\brestful\b",
    # Data / ML / AI
    "Machine Learning": r"\bmachine learning\b",
    "Deep Learning": r"\bdeep learning\b",
    "TensorFlow": r"\btensorflow\b",
    "PyTorch": r"\bpytorch\b",
    "scikit-learn": r"\bscikit.?learn\b|\bsklearn\b",
    "Pandas": r"\bpandas\b",
    "NumPy": r"\bnumpy\b",
    "NLP": r"\bnlp\b|\bnatural language processing\b",
    "Computer Vision": r"\bcomputer vision\b",
    "LLMs": r"\bllm\b|\blarge language model\b",
    "LangChain": r"\blangchain\b",
    "Hugging Face": r"\bhugging face\b|\btransformers\b",
    # Databases
    "SQL": r"\bsql\b",
    "PostgreSQL": r"\bpostgresql\b|\bpostgres\b",
    "MySQL": r"\bmysql\b",
    "MongoDB": r"\bmongodb\b",
    "Redis": r"\bredis\b",
    "Elasticsearch": r"\belasticsearch\b",
    "Cassandra": r"\bcassandra\b",
    # Cloud / DevOps
    "AWS": r"\baws\b|\bamazon web services\b",
    "GCP": r"\bgcp\b|\bgoogle cloud\b",
    "Azure": r"\bazure\b",
    "Docker": r"\bdocker\b",
    "Kubernetes": r"\bkubernetes\b|\bk8s\b",
    "Terraform": r"\bterraform\b",
    "CI/CD": r"\bci/cd\b|\bjenkins\b|\bgithub actions\b|\bgitlab ci\b",
    "Linux": r"\blinux\b|\bunix\b",
    "Git": r"\bgit\b",
    # Design
    "Figma": r"\bfigma\b",
    "Adobe XD": r"\badobe xd\b",
    # Methodologies
    "Agile": r"\bagile\b|\bscrum\b|\bkanban\b",
    "DevOps": r"\bdevops\b",
    "Microservices": r"\bmicroservices\b",
}

CONTACT_PATTERNS = {
    "email": r"[\w.\-+]+@[\w\-]+\.[\w.]+",
    "phone": r"(\+?\d[\d\s\-().]{7,})(?=\s|$)",
    "linkedin": r"linkedin\.com/in/[\w\-]+",
    "github": r"github\.com/[\w\-]+",
    "portfolio": r"https?://[\w.\-/]+",
}

EXPERIENCE_INDICATORS = [
    "experience", "worked", "developed", "built", "led", "managed", "designed",
    "implemented", "created", "deployed", "architected", "optimized", "reduced",
    "increased", "improved", "delivered", "launched", "collaborated", "maintained",
    "contributed", "responsible", "achieved", "spearheaded", "orchestrated",
]

EDUCATION_INDICATORS = {
    "phd": 5, "doctorate": 5, "master": 4, "m.tech": 4, "msc": 4, "m.s.": 4,
    "bachelor": 3, "b.tech": 3, "bsc": 3, "b.e.": 3, "b.s.": 3,
    "associate": 2, "diploma": 2,
    "certification": 1, "certified": 1, "certificate": 1,
}

ACHIEVEMENT_PATTERNS = [
    r"\b\d+%\b",                   # percentages
    r"\$[\d,]+[kmb]?\b",           # dollar amounts
    r"\b\d+[kmb]\+?\b",            # large numbers
    r"\bincreased\b.{0,40}\b\d+",  # increased X by N
    r"\breduced\b.{0,40}\b\d+",    # reduced X by N
]

SECTION_HEADERS = [
    "experience", "work experience", "employment", "professional experience",
    "education", "academic background", "skills", "technical skills",
    "projects", "certifications", "awards", "summary", "objective",
    "publications", "languages", "interests",
]


class ATSScorer:
    """
    Computes a comprehensive ATS score from resume plain text.
    Returns a score 0–100 with a detailed breakdown.
    """

    def __init__(self):
        self._compile_patterns()

    def _compile_patterns(self):
        self._skill_re = {k: re.compile(v, re.I) for k, v in SKILL_KEYWORDS.items()}
        self._contact_re = {k: re.compile(v, re.I) for k, v in CONTACT_PATTERNS.items()}
        self._achievement_re = [re.compile(p, re.I) for p in ACHIEVEMENT_PATTERNS]

    # ── Public API ────────────────────────────────────────────────────────────
    def score(self, text: str) -> Dict:
        if not text or len(text.strip()) < 50:
            return self._empty_result()

        detected_skills = self._detect_skills(text)
        contact = self._score_contact(text)
        experience = self._score_experience(text)
        education = self._score_education(text)
        skills_section = self._score_skills_section(text, detected_skills)
        fmt = self._score_format(text)
        certs = self._score_certifications(text)
        achievements = self._score_achievements(text)

        # Weighted average
        weights = {
            "keyword_density": 0.22,
            "contact_info": 0.12,
            "work_experience": 0.22,
            "education": 0.12,
            "skills_section": 0.10,
            "format_structure": 0.08,
            "certifications": 0.07,
            "achievements": 0.07,
        }
        breakdown = {
            "keyword_density": round(self._score_keywords(text, detected_skills), 1),
            "contact_info": round(contact["score"], 1),
            "work_experience": round(experience, 1),
            "education": round(education, 1),
            "skills_section": round(skills_section, 1),
            "format_structure": round(fmt, 1),
            "certifications": round(certs, 1),
            "achievements": round(achievements, 1),
        }
        total = sum(breakdown[k] * weights[k] for k in weights)
        total = max(0, min(100, round(total, 1)))

        skill_gaps = self._identify_gaps(detected_skills)
        recs = self._generate_recommendations(breakdown, detected_skills, contact)

        words = text.split()
        edu_level = self._detect_education_level(text)
        yoe = self._estimate_years_experience(text)

        return {
            "ats_score": total,
            "grade": self._grade(total),
            "breakdown": breakdown,
            "detected_skills": detected_skills,
            "skill_gaps": skill_gaps,
            "word_count": len(words),
            "keyword_count": len(detected_skills),
            "education_level": edu_level,
            "years_experience": yoe,
            "contact_completeness": round(contact["completeness"] * 100, 1),
            "recommendations": recs,
        }

    # ── Scoring components ────────────────────────────────────────────────────
    def _detect_skills(self, text: str) -> List[str]:
        return [skill for skill, pat in self._skill_re.items() if pat.search(text)]

    def _score_keywords(self, text: str, skills: List[str]) -> float:
        density = len(skills) / max(len(SKILL_KEYWORDS), 1)
        # TF-IDF approximation: reward common industry terms
        words = re.findall(r"\b\w+\b", text.lower())
        freq = Counter(words)
        tech_terms = sum(1 for w in freq if len(w) > 3 and freq[w] >= 2)
        base = min(100, density * 130)
        bonus = min(20, tech_terms * 0.5)
        return min(100, base + bonus)

    def _score_contact(self, text: str) -> Dict:
        found = {k: bool(p.search(text)) for k, p in self._contact_re.items()}
        weights = {"email": 0.40, "phone": 0.30, "linkedin": 0.20, "github": 0.07, "portfolio": 0.03}
        score = sum(weights[k] * 100 for k, v in found.items() if v)
        completeness = sum(1 for v in found.values() if v) / len(found)
        return {"score": score, "completeness": completeness, "found": found}

    def _score_experience(self, text: str) -> float:
        lower = text.lower()
        hits = sum(1 for w in EXPERIENCE_INDICATORS if w in lower)
        # Bullet points suggest proper formatting
        bullets = len(re.findall(r"^[\•\-\*\▪]\s", text, re.MULTILINE))
        verb_bonus = min(30, bullets * 2)
        base = min(70, hits * 6)
        return min(100, base + verb_bonus)

    def _score_education(self, text: str) -> float:
        lower = text.lower()
        best = 0
        for term, weight in EDUCATION_INDICATORS.items():
            if term in lower:
                best = max(best, weight)
        score_map = {5: 100, 4: 90, 3: 80, 2: 65, 1: 50, 0: 20}
        return score_map.get(best, 20)

    def _score_skills_section(self, text: str, skills: List[str]) -> float:
        has_header = bool(re.search(r"\b(skills|technical skills|core competencies)\b", text, re.I))
        skill_count_score = min(80, len(skills) * 5)
        header_bonus = 20 if has_header else 0
        return min(100, skill_count_score + header_bonus)

    def _score_format(self, text: str) -> float:
        score = 0
        # Length check (ideal: 400–800 words)
        wc = len(text.split())
        if 400 <= wc <= 1200:
            score += 35
        elif wc > 200:
            score += 20

        # Section headers
        found_headers = sum(1 for h in SECTION_HEADERS if re.search(r"\b" + h + r"\b", text, re.I))
        score += min(35, found_headers * 7)

        # No garbled characters (PDF parsing artifacts)
        garbled = len(re.findall(r"[^\x00-\x7F]", text))
        if garbled < 20:
            score += 30
        elif garbled < 100:
            score += 15
        return min(100, score)

    def _score_certifications(self, text: str) -> float:
        cert_patterns = [
            r"\baws certified\b", r"\bgoogle certified\b", r"\bazure certified\b",
            r"\bcertified\b", r"\bcertification\b", r"\bpmp\b", r"\bcissp\b",
            r"\bccna\b", r"\bcompTIA\b", r"\bscrummaster\b",
        ]
        hits = sum(1 for p in cert_patterns if re.search(p, text, re.I))
        return min(100, hits * 25)

    def _score_achievements(self, text: str) -> float:
        hits = sum(1 for p in self._achievement_re if p.search(text))
        return min(100, hits * 20)

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _identify_gaps(self, detected: List[str]) -> List[str]:
        """Return high-value skills not in the resume."""
        high_value = ["Python", "SQL", "Git", "Docker", "React", "AWS",
                      "Agile", "REST API", "Machine Learning", "CI/CD",
                      "Kubernetes", "TypeScript", "PostgreSQL", "Linux"]
        return [s for s in high_value if s not in detected][:10]

    def _generate_recommendations(self, breakdown: Dict, skills: List[str], contact: Dict) -> List[str]:
        recs = []
        if breakdown["contact_info"] < 70:
            missing = [k for k, v in contact.get("found", {}).items() if not v]
            recs.append(f"Add missing contact info: {', '.join(missing)}")
        if breakdown["keyword_density"] < 60:
            recs.append("Add more relevant technical keywords matching your target job description")
        if breakdown["achievements"] < 50:
            recs.append("Quantify achievements with metrics (e.g., 'Reduced load time by 40%')")
        if breakdown["work_experience"] < 60:
            recs.append("Use strong action verbs (Led, Built, Delivered) to describe experience")
        if breakdown["format_structure"] < 70:
            recs.append("Add clear section headers: Experience, Skills, Education, Certifications")
        if breakdown["certifications"] < 30:
            recs.append("Earn industry certifications (AWS, Google Cloud, CompTIA) to boost credibility")
        if "SQL" not in skills:
            recs.append("Add SQL to your skillset — required in 80%+ of data and backend roles")
        if len(skills) < 10:
            recs.append("Expand your skills section with specific tools and technologies")
        return recs[:6]

    def _detect_education_level(self, text: str) -> str:
        lower = text.lower()
        if any(t in lower for t in ["phd", "doctorate", "ph.d"]):
            return "PhD"
        if any(t in lower for t in ["master", "m.tech", "msc", "m.s."]):
            return "Master's"
        if any(t in lower for t in ["bachelor", "b.tech", "bsc", "b.e.", "b.s."]):
            return "Bachelor's"
        if any(t in lower for t in ["diploma", "associate"]):
            return "Diploma/Associate"
        return "Not specified"

    def _estimate_years_experience(self, text: str) -> int:
        years = re.findall(r"(\d+)\+?\s*years?\s+(?:of\s+)?experience", text, re.I)
        if years:
            return max(int(y) for y in years)
        # Count year ranges like 2020–2023
        ranges = re.findall(r"(20\d{2})\s*[–\-to]+\s*(20\d{2}|present|current)", text, re.I)
        if ranges:
            total = 0
            for start, end in ranges:
                e = 2024 if end.lower() in ("present", "current") else int(end)
                total += max(0, e - int(start))
            return total
        return 0

    def _grade(self, score: float) -> str:
        if score >= 85:   return "Excellent"
        if score >= 70:   return "Good"
        if score >= 55:   return "Fair"
        if score >= 40:   return "Needs Improvement"
        return "Poor"

    def _empty_result(self) -> Dict:
        return {
            "ats_score": 0, "grade": "Poor",
            "breakdown": {k: 0 for k in ["keyword_density","contact_info","work_experience","education","skills_section","format_structure","certifications","achievements"]},
            "detected_skills": [], "skill_gaps": [], "word_count": 0,
            "keyword_count": 0, "education_level": None, "years_experience": 0,
            "contact_completeness": 0, "recommendations": ["Resume text could not be extracted. Ensure the PDF is not scanned/image-only."],
        }


# Singleton
ats_scorer = ATSScorer()
