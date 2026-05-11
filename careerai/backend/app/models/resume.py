"""Resume data models and schemas"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class ATSBreakdown(BaseModel):
    keyword_density: float = 0
    contact_info: float = 0
    work_experience: float = 0
    education: float = 0
    skills_section: float = 0
    format_structure: float = 0
    certifications: float = 0
    achievements: float = 0

class ResumeAnalysis(BaseModel):
    ats_score: float
    grade: str
    breakdown: ATSBreakdown
    detected_skills: List[str] = []
    skill_gaps: List[str] = []
    extracted_text: str = ""
    word_count: int = 0
    page_count: int = 0
    education_level: Optional[str] = None
    years_experience: Optional[int] = None
    contact_completeness: float = 0
    keyword_count: int = 0
    recommendations: List[str] = []

class CareerMatch(BaseModel):
    title: str
    match_score: float
    salary_range: str
    demand_level: str
    required_skills: List[str]
    matching_skills: List[str]
    missing_skills: List[str]
    description: str
    growth_rate: str

class ResumeInDB(BaseModel):
    id: Optional[str] = None
    user_id: str
    filename: str
    file_path: str
    file_size: int
    file_type: str
    analysis: Optional[ResumeAnalysis] = None
    career_matches: List[CareerMatch] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ResumeResponse(BaseModel):
    id: str
    filename: str
    file_size: int
    analysis: ResumeAnalysis
    career_matches: List[CareerMatch]
    created_at: datetime
