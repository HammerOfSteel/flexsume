from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    created_at = Column(Date)
    updated_at = Column(Date)

    competencies = relationship("Competency", back_populates="user")
    experiences = relationship("Experience", back_populates="user")
    educations = relationship("Education", back_populates="user")
    projects = relationship("Project", back_populates="user")
    resumes = relationship("Resume", back_populates="user")

class Competency(Base):
    __tablename__ = "competencies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    description = Column(Text)
    proficiency_level = Column(String)
    created_at = Column(Date)
    updated_at = Column(Date)

    user = relationship("User", back_populates="competencies")

class Experience(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    company = Column(String)
    location = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(Text)
    created_at = Column(Date)
    updated_at = Column(Date)

    user = relationship("User", back_populates="experiences")

class Education(Base):
    __tablename__ = "Education"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    institute = Column(String)
    location = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(Text)
    created_at = Column(Date)
    updated_at = Column(Date)

    user = relationship("User", back_populates="educations")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    url = Column(String)
    created_at = Column(Date)
    updated_at = Column(Date)

    user = relationship("User", back_populates="projects")

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    description = Column(Text)
    created_at = Column(Date)
    updated_at = Column(Date)

    user = relationship("User", back_populates="resumes")
    sections = relationship("ResumeSection", back_populates="resume")

class ResumeSection(Base):
    __tablename__ = "resume_sections"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    section_type = Column(String)
    section_id = Column(Integer)
    order = Column(Integer)
    created_at = Column(Date)
    updated_at = Column(Date)

    resume = relationship("Resume", back_populates="sections")