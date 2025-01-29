from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: str
    start_date: str
    end_date: Optional[str] = None
    gpa: Optional[float] = None

class Experience(BaseModel):
    company: str
    position: str
    start_date: str
    end_date: Optional[str] = None
    description: List[str]

class Skill(BaseModel):
    category: str
    skills: List[str]

class ResumeData(BaseModel):
    template_name: Literal["ats_friendly", "modern_ats", "classic", "professional_ats", "modern_two_column"] = Field(
        description="Choose template style: ats_friendly, modern_ats, classic, professional_ats, or modern_two_column"
    )
    full_name: str
    profession: Optional[str] = None
    email: str
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    summary: str
    education: List[Education]
    experience: List[Experience]
    skills: List[Skill] 