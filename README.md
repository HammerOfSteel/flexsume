# Flexsume
Flexsume is a composable and, most of all, flexible resume builder. Save your competencies, experiences, and projects. Build a resume perfect for that next role.

## Overview
Flexsume is a modern, web-based resume builder that allows users to create, manage, and customize their resumes with ease. The application focuses on flexibility and composability, enabling users to tailor their resumes to specific job roles or industries.

Users can input and save their competencies, work experiences, and projects, which can then be used to generate targeted resumes. The application provides a user-friendly interface for creating and editing resume sections, as well as customizing the layout and design of the generated resumes.

# Architecture Design
## Frontend
- Server-rendered HTML pages with HTMX for interactive and dynamic content
- Minimal JavaScript for enhanced user experience
- Responsive design with CSS frameworks like Bootstrap or Tailwind CSS
- Integration with backend API using HTMX's AJAX capabilities

## Backend
- RESTful API built with FastAPI, a modern, fast (high-performance) Python web framework
- Database management using PostgreSQL, a powerful, open-source relational database system
- Authentication and authorization using JSON Web Tokens (JWT)
- API documentation using Swagger UI and OpenAPI


## Infrastructure
- Containerization using Docker for easy deployment and scalability
- Hosting on cloud platforms like AWS, Google Cloud, or Heroku
- Continuous Integration and Continuous Deployment (CI/CD) using tools like Jenkins, GitLab CI, or Travis CI

## Tech Stack
Frontend:
- HTML
- HTMX
- Bootstrap or Tailwind CSS

Backend:
- FastAPI
- Python
- PostgreSQL
- JSON Web Tokens (JWT)
- Swagger UI and OpenAPI

Infrastructure:
- Docker
- AWS, Google Cloud, or Heroku
- Jenkins, GitLab CI, or Travis CI

# Getting Started
1. Clone the repository
2. Install dependencies for frontend and backend
3. Set up the PostgreSQL database and environment variables
4. Run the FastAPI development server
5. Access the application in your browser