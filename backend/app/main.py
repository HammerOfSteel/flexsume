from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models import Base, User, Competency, Experience, Project, Resume, ResumeSection
from app.database import SessionLocal, engine
from app import models, schemas
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import date  # Add this import
from fastapi import FastAPI, Response
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import StreamingResponse
from fpdf import FPDF, HTMLMixin
from io import BytesIO
import html
logging.basicConfig(level=logging.DEBUG)

models.Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a sample user and their data
@app.on_event("startup")
def create_sample_data():
    db = SessionLocal()
    
    # Create a sample user
    sample_user = models.User(
        email="sample@example.com",
        hashed_password="samplepassword",
        first_name="John",
        last_name="Doe",
        created_at=date.today(),
        updated_at=date.today()
    )
    db.add(sample_user)
    db.commit()
    db.refresh(sample_user)

    # Create sample competencies for the user
    sample_competencies = [
        models.Competency(
            user_id=sample_user.id,
            name="Programming",
            description="Proficient in Python and JavaScript",
            proficiency_level="Advanced",
            created_at=date.today(),
            updated_at=date.today()
        ),
        models.Competency(
            user_id=sample_user.id,
            name="Database Management",
            description="Experience with MySQL and PostgreSQL",
            proficiency_level="Intermediate",
            created_at=date.today(),
            updated_at=date.today()
        )
    ]
    db.add_all(sample_competencies)
    db.commit()

    # Create sample experiences for the user
    sample_experiences = [
        models.Experience(
            user_id=sample_user.id,
            title="Software Engineer",
            company="ABC Company",
            location="New York",
            start_date=date(2020, 1, 1),
            end_date=date(2022, 12, 31),
            description="Developed and maintained web applications",
            created_at=date.today(),
            updated_at=date.today()
        ),
        models.Experience(
            user_id=sample_user.id,
            title="Data Analyst",
            company="XYZ Corporation",
            location="London",
            start_date=date(2018, 6, 1),
            end_date=date(2019, 12, 31),
            description="Analyzed and visualized data using Python",
            created_at=date.today(),
            updated_at=date.today()
        )
    ]
    db.add_all(sample_experiences)
    db.commit()

    # Create sample projects for the user
    sample_projects = [
        models.Project(
            user_id=sample_user.id,
            title="Portfolio Website",
            description="Personal portfolio website showcasing projects",
            start_date=date(2022, 1, 1),
            end_date=date(2022, 3, 31),
            url="https://example.com/portfolio",
            created_at=date.today(),
            updated_at=date.today()
        ),
        models.Project(
            user_id=sample_user.id,
            title="Machine Learning Project",
            description="Implemented a machine learning model for prediction",
            start_date=date(2021, 6, 1),
            end_date=date(2021, 8, 31),
            url="https://github.com/example/ml-project",
            created_at=date.today(),
            updated_at=date.today()
        )
    ]
    db.add_all(sample_projects)
    db.commit()

    db.close()


class Section(BaseModel):
    section_type: str
    order: int

class ResumeData(BaseModel):
    name: str = Field(default="John Doe")
    description: str
    competencies: List[dict]
    experiences: List[dict]
    projects: List[dict]
        
@app.post("/api/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Hardcoded username and password
    valid_username = "terry"
    valid_password = "goleman"

    if form_data.username == valid_username and form_data.password == valid_password:
        # Authentication successful
        return {"access_token": "dummy_token", "token_type": "bearer"}
    else:
        # Authentication failed
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@app.post("/competencies/", response_model=schemas.Competency)
def create_competency(competency: schemas.CompetencyCreate, db: Session = Depends(get_db)):
    db_competency = models.Competency(**competency.dict())
    db_competency.user_id = 1  # Set the appropriate user_id
    db_competency.created_at = date.today()
    db_competency.updated_at = date.today()
    db.add(db_competency)
    db.commit()
    db.refresh(db_competency)
    return db_competency

@app.get("/competencies/", response_model=list[schemas.Competency])
def read_competencies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    competencies = db.query(models.Competency).offset(skip).limit(limit).all()
    return competencies

@app.post("/experiences/", response_model=schemas.Experience)
def create_experience(experience: schemas.ExperienceCreate, db: Session = Depends(get_db)):
    db_experience = models.Experience(**experience.dict())
    db_experience.user_id = 1  # Set the appropriate user_id
    db_experience.created_at = date.today()
    db_experience.updated_at = date.today()
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)
    return db_experience


@app.get("/experiences/", response_model=list[schemas.Experience])
def read_experiences(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    experiences = db.query(models.Experience).offset(skip).limit(limit).all()
    return experiences

@app.post("/projects/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    db_project = models.Project(**project.dict())
    db_project.user_id = 1  # Set the appropriate user_id
    db_project.created_at = date.today()
    db_project.updated_at = date.today()
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.get("/projects/", response_model=list[schemas.Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = db.query(models.Project).offset(skip).limit(limit).all()
    return projects

@app.post("/resumes/", response_model=schemas.Resume)
def create_resume(resume: schemas.ResumeCreate, db: Session = Depends(get_db)):
    db_resume = models.Resume(
        user_id=1,  # Set the appropriate user_id
        name=resume.name,
        description=resume.description,
        created_at=date.today(),
        updated_at=date.today()
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)

    for section in resume.sections:
        db_section = models.ResumeSection(
            resume_id=db_resume.id,
            section_type=section.section_type,
            section_id=section.section_id,
            order=section.order,
            created_at=date.today(),
            updated_at=date.today()
        )
        db.add(db_section)

    db.commit()
    db.refresh(db_resume)
    return db_resume

@app.get("/resumes/", response_model=list[schemas.Resume])
def read_resumes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    resumes = db.query(models.Resume).offset(skip).limit(limit).all()
    return resumes

@app.post("/resume-sections/", response_model=schemas.ResumeSection)
def create_resume_section(resume_section: schemas.ResumeSectionCreate, db: Session = Depends(get_db)):
    db_resume_section = models.ResumeSection(**resume_section.dict())
    db_resume_section.user_id = 1  # Set the appropriate user_id
    db_resume_section.created_at = date.today()
    db_resume_section.updated_at = date.today()
    db.add(db_resume_section)
    db.commit()
    db.refresh(db_resume_section)
    return db_resume_section

@app.get("/resume-sections/", response_model=list[schemas.ResumeSection])
def read_resume_sections(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    resume_sections = db.query(models.ResumeSection).offset(skip).limit(limit).all()
    return resume_sections