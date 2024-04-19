from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    first_name: str
    last_name: str
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True

class CompetencyBase(BaseModel):
    name: str
    description: str
    proficiency_level: str

class CompetencyCreate(CompetencyBase):
    pass

class Competency(CompetencyBase):
    id: int
    user_id: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True

class ExperienceBase(BaseModel):
    title: str
    company: str
    location: str
    start_date: date
    end_date: date
    description: str

class ExperienceCreate(ExperienceBase):
    pass

class Experience(ExperienceBase):
    id: int
    user_id: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True

class EducationBase(BaseModel):
    title: str
    institute: str
    location: str
    start_date: date
    end_date: date
    description: str

class EducationCreate(EducationBase):
    pass

class Education(EducationBase):
    id: int
    user_id: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    title: str
    description: str
    start_date: date
    end_date: date
    url: str

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    user_id: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True

class ResumeSectionBase(BaseModel):
    section_type: str
    section_id: int
    order: int

class ResumeSectionCreate(ResumeSectionBase):
    pass

class ResumeSection(ResumeSectionBase):
    id: int
    resume_id: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True

class ResumeBase(BaseModel):
    name: str
    description: str
    fullname: Optional[str]
    jobtitle: Optional[str]
    jobtitledescription: Optional[str]
    summary: Optional[str]

class ResumeSectionCreate(BaseModel):
    section_type: str
    section_id: int
    order: int

class ResumeCreate(BaseModel):
    name: str
    description: str
    fullname: Optional[str]
    jobtitle: Optional[str]
    jobtitledescription: Optional[str]
    summary: Optional[str]
    sections: List[ResumeSectionCreate]
    
class Resume(ResumeBase):
    id: int
    user_id: int
    created_at: date
    updated_at: date
    sections: list[ResumeSection] = []

    class Config:
        from_attributes = True