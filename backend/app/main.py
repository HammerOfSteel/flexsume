from fastapi import FastAPI, Depends, HTTPException, status
from fastapi import FastAPI, Request, HTTPException, Depends, status
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
from datetime import date
import html
import os
import dotenv
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, Request, HTTPException, status
from pydantic import BaseModel
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.middleware.sessions import SessionMiddleware
logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

# load .env file
dotenv.load_dotenv()

# Constants and Application setup
SAMPLE_USER_FIRSTNAME = os.getenv("SAMPLE_USER_FIRSTNAME")
SAMPLE_USER_LASTNAME = os.getenv("SAMPLE_USER_LASTNAME")
SAMPLE_USER_EMAIL = os.getenv("SAMPLE_USER_EMAIL")
SAMPLE_USER_PASS = os.getenv("SAMPLE_USER_PASS")
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY")

models.Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)

global userID
if userID is None:
    userID = 1

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
            email=SAMPLE_USER_EMAIL,
            hashed_password=SAMPLE_USER_PASS,
            first_name=SAMPLE_USER_FIRSTNAME,
            last_name=SAMPLE_USER_LASTNAME,
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
    

class currentUser(BaseModel):
    id: int  # User ID
    name: str
    email: str

@app.post("/user")
async def receive_user_data(user: currentUser, request: Request):
    try:
        request.session['user'] = user.dict()
        request.session['user_id'] = user.id
        global userID
        userID = user.id
        return JSONResponse(status_code=HTTP_201_CREATED, content={"message": "User data received and session updated"})
    except AssertionError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="SessionMiddleware not installed")


def get_current_user(request: Request):
    user_id = request.session.get('user_id')
    logging.debug(f"User ID from session: {user_id}")
    if not user_id:
        user_id = userID
        logging.debug(f"User ID now found in session as a global variable {user_id}")
    return user_id

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), request: Request = None):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_id = get_current_user(request)
    db_user = models.User(
        id=user_id,
        email=user.email,
        hashed_password=user.password,
        first_name=user.first_name,
        last_name=user.last_name,
        created_at=date.today(),  # Set the created_at field with today's date
        updated_at=date.today()   # Set the updated_at field with today's date
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users


@app.post("/competencies/", response_model=schemas.Competency)
def create_competency(competency: schemas.CompetencyCreate, db: Session = Depends(get_db), request: Request = None):
    user_id = userID 
    db_competency = models.Competency(**competency.dict())
    db_competency.user_id = int(user_id)
    db_competency.created_at = date.today()
    db_competency.updated_at = date.today()
    db.add(db_competency)
    db.commit()
    db.refresh(db_competency)
    return db_competency


@app.get("/competencies/", response_model=list[schemas.Competency])
async def read_competencies(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Extracting user ID from the request header
    user_id = userID
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID header is missing")
    try:
        user_id = int(user_id)  # Ensure the user_id is an integer
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    # Fetch only competencies that belong to the specified user_id
    competencies = db.query(models.Competency).filter(models.Competency.user_id.in_([1,user_id])).offset(skip).limit(limit).all()
    return competencies


@app.post("/experiences/", response_model=schemas.Experience)
def create_experience(experience: schemas.ExperienceCreate, db: Session = Depends(get_db), request: Request = None):
    user_id = userID
    db_experience = models.Experience(**experience.dict())
    db_experience.user_id = int(user_id)
    db_experience.created_at = date.today()
    db_experience.updated_at = date.today()
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)
    return db_experience


@app.get("/experiences/", response_model=list[schemas.Experience])
def read_experiences(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Extracting user ID from the request header
    user_id = userID
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID header is missing")
    try:
        user_id = int(user_id)  # Ensure the user_id is an integer
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    experiences = db.query(models.Experience).filter(models.Experience.user_id.in_([1,user_id])).offset(skip).limit(limit).all()
    return experiences


@app.post("/educations/", response_model=schemas.Education)
def create_education(education: schemas.EducationCreate, db: Session = Depends(get_db), request: Request = None):
    user_id = userID
    db_education = models.Education(**education.dict())
    db_education.user_id = int(user_id)
    db_education.created_at = date.today()
    db_education.updated_at = date.today()
    db.add(db_education)
    db.commit()
    db.refresh(db_education)
    return db_education


@app.get("/educations/", response_model=list[schemas.Education])
def read_educations(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Extracting user ID from the request header
    user_id = userID
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID header is missing")
    try:
        user_id = int(user_id)  # Ensure the user_id is an integer
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    educations = db.query(models.Education).filter(models.Education.user_id.in_([1,user_id])).offset(skip).limit(limit).all()
    return educations


@app.post("/projects/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db), request: Request = None):
    user_id = userID
    db_project = models.Project(**project.dict())
    db_project.user_id = int(user_id)
    db_project.created_at = date.today()
    db_project.updated_at = date.today()
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.get("/projects/", response_model=list[schemas.Project])
def read_projects(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Extracting user ID from the request header
    user_id = userID
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID header is missing")
    try:
        user_id = int(user_id)  # Ensure the user_id is an integer
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    projects = db.query(models.Project).filter(models.Project.user_id.in_([1,user_id])).offset(skip).limit(limit).all()
    return projects

@app.post("/resumes/", response_model=schemas.Resume)
def create_resume(resume: schemas.ResumeCreate, db: Session = Depends(get_db), request: Request = None):
    user_id = userID
    db_resume = models.Resume(
        user_id=int(user_id),
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
def read_resumes(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Extracting user ID from the request header
    user_id = userID
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID header is missing")
    try:
        user_id = int(user_id)  # Ensure the user_id is an integer
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    resumes = db.query(models.Resume).filter(models.Resume.user_id.in_([1,user_id])).offset(skip).limit(limit).all()
    return resumes

@app.get("/resumes/{resume_id}", response_model=schemas.Resume)
def read_resume(request: Request, resume_id: int, db: Session = Depends(get_db)):
    # Extracting user ID from the request header
    user_id = userID
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID header is missing")
    try:
        user_id = int(user_id)  # Ensure the user_id is an integer
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    resume = db.query(models.Resume).filter(models.Resume.user_id.in_([1,user_id])).filter(models.Resume.id == resume_id).first()
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume

@app.post("/resume-sections/", response_model=schemas.ResumeSection)
def create_resume_section(resume_section: schemas.ResumeSectionCreate, db: Session = Depends(get_db), request: Request = None):
    user_id = userID
    db_resume_section = models.ResumeSection(**resume_section.dict())
    db_resume_section.user_id = int(user_id)
    db_resume_section.created_at = date.today()
    db_resume_section.updated_at = date.today()
    db.add(db_resume_section)
    db.commit()
    db.refresh(db_resume_section)
    return db_resume_section

@app.get("/resume-sections/", response_model=list[schemas.ResumeSection])
def read_resume_sections(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Extracting user ID from the request header
    user_id = userID
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID header is missing")
    try:
        user_id = int(user_id)  # Ensure the user_id is an integer
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    resume_sections = db.query(models.ResumeSection).filter(models.ResumeSection.user_id.in_([1,user_id])).offset(skip).limit(limit).all()
    return resume_sections

# FastAPI route to get a specific competency by ID
@app.get("/competencies/{competency_id}", response_model=schemas.Competency)
def read_competency(request: Request, competency_id: int, db: Session = Depends(get_db)):
    # Extracting user ID from the request header
    user_id = userID
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID header is missing")
    try:
        user_id = int(user_id)  # Ensure the user_id is an integer
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    competency = db.query(models.Competency).filter(models.Competency.user_id.in_([1,user_id])).filter(models.Competency.id == competency_id).first()
    if competency is None:
        raise HTTPException(status_code=404, detail="Competency not found")
    return competency

# FastAPI route to get a specific experience by ID
@app.get("/experiences/{experience_id}", response_model=schemas.Experience)
def read_experience(request: Request, experience_id: int, db: Session = Depends(get_db)):
    # Extracting user ID from the request header
    user_id = userID
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID header is missing")
    try:
        user_id = int(user_id)  # Ensure the user_id is an integer
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    experience = db.query(models.Experience).filter(models.Experience.user_id.in_([1,user_id])).filter(models.Experience.id == experience_id).first()
    if experience is None:
        raise HTTPException(status_code=404, detail="Experience not found")
    return experience

# FastAPI route to get a specific education by ID
@app.get("/educations/{education_id}", response_model=schemas.Education)
def read_education(request: Request, education_id: int, db: Session = Depends(get_db)):
    # Extracting user ID from the request header
    user_id = userID
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID header is missing")
    try:
        user_id = int(user_id)  # Ensure the user_id is an integer
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    education = db.query(models.Education).filter(models.Education.user_id.in_([1,user_id])).filter(models.Education.id == education_id).first()
    if education is None:
        raise HTTPException(status_code=404, detail="Education not found")
    return education

# FastAPI route to get a specific project by ID
@app.get("/projects/{project_id}", response_model=schemas.Project)
def read_project(request: Request, project_id: int, db: Session = Depends(get_db)):
    # Extracting user ID from the request header
    user_id = userID
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID header is missing")
    try:
        user_id = int(user_id)  # Ensure the user_id is an integer
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    project = db.query(models.Project).filter(models.Project.user_id.in_([1,user_id])).filter(models.Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

# FastAPI route to get a specific competency by ID
@app.get("/competencys/{competency_id}", response_model=schemas.Competency)
def read_competency(request: Request, competency_id: int, db: Session = Depends(get_db)):
    # Extracting user ID from the request header
    user_id = userID
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID header is missing")
    try:
        user_id = int(user_id)  # Ensure the user_id is an integer
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    competency = db.query(models.Competency).filter(models.Competency.user_id.in_([1,user_id])).filter(models.Competency.id == competency_id).first()
    if competency is None:
        raise HTTPException(status_code=404, detail="Competency not found")
    return competency
