from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class PositionRecommendation(BaseModel):
    title: str
    justification: str

class CompetencyComparison(BaseModel):
    current_skills: List[str]
    required_skills: List[str]
    gap_analysis: str

class DevelopmentPlan(BaseModel):
    timeline: str
    learning_areas: List[str]
    projects: List[str]
    milestones: List[str]

class CourseRecommendation(BaseModel):
    title: str
    description: str
    duration: str
    platform: str

class VacancyRecommendation(BaseModel):
    title: str
    company: str
    experience_required: str
    key_skills: List[str]
    match_score: int

class CareerRecommendations(BaseModel):
    nearest_position: PositionRecommendation
    recommended_position: PositionRecommendation
    competency_comparison: CompetencyComparison
    development_plan: DevelopmentPlan
    recommended_courses: List[CourseRecommendation]
    relevant_vacancies: List[VacancyRecommendation]
    user_stats: Optional[Dict[str, Any]] = None
    skills_data: Optional[Dict[str, Any]] = None
    roadmap_data: Optional[Dict[str, Any]] = None

class UserContext(BaseModel):
    current_skills: Optional[List[str]] = None
    experience: Optional[str] = None
    current_position: Optional[str] = None
    goals: Optional[str] = None
    interests: Optional[List[str]] = None

class RecommendationRequest(BaseModel):
    user_context: UserContext
    target_position: Optional[str] = None
    top_k_vacancies: int = 5

class RecommendationResponse(BaseModel):
    recommendations: CareerRecommendations
    status: str = "success"
    message: Optional[str] = None
