from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models import Base, User, Competency, Experience, Project, Resume, ResumeSection, Education
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
    try:
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

        # Create sample education for the user
        sample_education = [
            models.Education(
                user_id=sample_user.id,
                title="Software Engineer",
                institute="University of California, Berkeley",
                location="Berkeley",
                start_date=date(2020, 1, 1),
                end_date=date(2022, 12, 31),
                description="Studied computer science at the University of California, Berkeley",
                created_at=date.today(),
                updated_at=date.today()
            ),
            models.Education(
                user_id=sample_user.id,
                title="Data Analyst",
                institute="Certification for Data Analyst",
                location="Udemy",
                start_date=date(2018, 6, 1),
                end_date=date(2019, 12, 31),
                description="Obtained a certification in data analysis",
                created_at=date.today(),
                updated_at=date.today()
            )
        ]
        db.add_all(sample_education)
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

        # save some resumes containing sample data with experiences, educations, and projects
        resume1 = models.Resume(
            user_id=sample_user.id,
            name="Resume 1",
            description="A resume with some experiences and projects",
            fullname="John Doe",
            jobtitle="DevOps Engineer",
            jobtitledescription="I am a DevOps Engineer with 5 years of experience",
            summary="I am a summary with some key competencies and experiences",
            created_at=date.today(),
            updated_at=date.today()
        )
        db.add(resume1)
        db.commit()
        db.refresh(resume1)

        resume1_sections = [
            models.ResumeSection(
                resume_id=resume1.id,
                section_type="experience",
                section_id=1,
                order=1,
                created_at=date.today(),
                updated_at=date.today()
            ),
            models.ResumeSection(
                resume_id=resume1.id,
                section_type="education",
                section_id=1,
                order=2,
                created_at=date.today(),
                updated_at=date.today()
            ),
            models.ResumeSection(
                resume_id=resume1.id,
                section_type="project",
                section_id=1,
                order=3,
                created_at=date.today(),
                updated_at=date.today()
            ),
            models.ResumeSection(
                resume_id=resume1.id,
                section_type="competency",
                section_id=1,
                order=4,
                created_at=date.today(),
                updated_at=date.today()
            )
        ]
        db.add_all(resume1_sections)
        db.commit()

        # another resume:
        resume2 = models.Resume(
            user_id=sample_user.id,
            name="Resume 2",
            description="Another resume with some experiences and projects",
            fullname="John Smith",
            jobtitle="Software Engineer",
            jobtitledescription="Developed and maintained web applications",
            summary="Analyzed and visualized data using Python",
            created_at=date.today(),
            updated_at=date.today()
        )
        db.add(resume2)
        db.commit()
        db.refresh(resume2)

        resume2_sections = [
            models.ResumeSection(
                resume_id=resume2.id,
                section_type="experience",
                section_id=1,
                order=1,
                created_at=date.today(),
                updated_at=date.today()
            ),
            models.ResumeSection(
                resume_id=resume2.id,
                section_type="education",
                section_id=1,
                order=2,
                created_at=date.today(),
                updated_at=date.today() # add this line
            ),
            models.ResumeSection(
                resume_id=resume2.id,
                section_type="project",
                section_id=1,
                order=3,
                created_at=date.today(),
                updated_at=date.today()
            ),
            models.ResumeSection(
                resume_id=resume2.id,
                section_type="competency",
                section_id=1,
                order=4,
                created_at=date.today(),
                updated_at=date.today()
            )
        ]
        db.add_all(resume2_sections)
        db.commit()
        db.close()
    except Exception as e:
        print(f"Startup data already exists. Error: {e}")
        db.rollback()
    finally:
        db.close()


class Section(BaseModel):
    section_type: str
    order: int

class ResumeData(BaseModel):
    name: str = Field(default="John Doe")
    description: str
    fullname: Optional[str]
    jobtitle: Optional[str]
    jobtitledescription: Optional[str]
    summary: Optional[str]
    competencies: List[dict]
    experiences: List[dict]
    educations: List[dict]
    projects: List[dict]


class LoginSchema(BaseModel):
    username: str
    password: str
        
@app.post("/api/login")
def login(login_data: LoginSchema):
    # Hardcoded username and password
    valid_username = "user@example.com"
    valid_password = "password"

    if login_data.username == valid_username and login_data.password == valid_password:
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


@app.post("/educations/", response_model=schemas.Education)
def create_education(education: schemas.EducationCreate, db: Session = Depends(get_db)):
    db_education = models.Education(**education.dict())
    db_education.user_id = 1  # Set the appropriate user_id
    db_education.created_at = date.today()
    db_education.updated_at = date.today()
    db.add(db_education)
    db.commit()
    db.refresh(db_education)
    return db_education


@app.get("/educations/", response_model=list[schemas.Education])
def read_educations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    educations = db.query(models.Education).offset(skip).limit(limit).all()
    return educations


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
        user_id=1,  # You might want to dynamically set this based on logged-in user
        name=resume.name,
        description=resume.description,
        fullname=resume.fullname,
        jobtitle=resume.jobtitle,
        jobtitledescription=resume.jobtitledescription,
        summary=resume.summary,
        created_at=date.today(),
        updated_at=date.today()
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)

    # Handling sections
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

    return db_resume


@app.get("/resumes/", response_model=list[schemas.Resume])
def read_resumes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    resumes = db.query(models.Resume).offset(skip).limit(limit).all()
    return resumes

@app.get("/resumes/{resume_id}", response_model=schemas.Resume)
def read_resume(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(models.Resume).filter(models.Resume.id == resume_id).first()
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume

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

# FastAPI route to get a specific competency by ID
@app.get("/competencies/{competency_id}", response_model=schemas.Competency)
def read_competency(competency_id: int, db: Session = Depends(get_db)):
    competency = db.query(models.Competency).filter(models.Competency.id == competency_id).first()
    if competency is None:
        raise HTTPException(status_code=404, detail="Competency not found")
    return competency

# FastAPI route to get a specific experience by ID
@app.get("/experiences/{experience_id}", response_model=schemas.Experience)
def read_experience(experience_id: int, db: Session = Depends(get_db)):
    experience = db.query(models.Experience).filter(models.Experience.id == experience_id).first()
    if experience is None:
        raise HTTPException(status_code=404, detail="Experience not found")
    return experience

# FastAPI route to get a specific education by ID
@app.get("/educations/{education_id}", response_model=schemas.Education)
def read_education(education_id: int, db: Session = Depends(get_db)):
    education = db.query(models.Education).filter(models.Education.id == education_id).first()
    if education is None:
        raise HTTPException(status_code=404, detail="Education not found")
    return education

# FastAPI route to get a specific project by ID
@app.get("/projects/{project_id}", response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

# FastAPI route to get a specific competency by ID
@app.get("/competencys/{competency_id}", response_model=schemas.Competency)
def read_competency(competency_id: int, db: Session = Depends(get_db)):
    competency = db.query(models.Competency).filter(models.Competency.id == competency_id).first()
    if competency is None:
        raise HTTPException(status_code=404, detail="Competency not found")
    return competency
