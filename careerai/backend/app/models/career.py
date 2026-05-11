from pydantic import BaseModel
from typing import List, Optional

class CareerMatch(BaseModel):
    title: str
    match_score: float
    salary_range: str
    demand_level: str
    required_skills: List[str]
    missing_skills: List[str]
    description: str
    growth_rate: str
    remote_friendly: bool

class SkillGapAnalysis(BaseModel):
    career: str
    current_skills: List[str]
    required_skills: List[str]
    missing_skills: List[str]
    gap_percentage: float
    estimated_months: int
    recommended_courses: List[dict]

class LearningRoadmap(BaseModel):
    career: str
    total_steps: int
    estimated_months: int
    steps: List[dict]
