from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.security.oauth2 import OAuth2AuthorizationCodeBearer
import aiohttp
import uvicorn
import ssl
import logging
import os
from fastapi.responses import Response
from fastapi import FastAPI, HTTPException
from typing import Union
import asyncpg
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi import FastAPI, HTTPException
from asyncpg import Connection, connect
from asyncpg.exceptions import PostgresError  # Correct import for handling errors
from pydantic import BaseModel, EmailStr, Field
from fastapi.security import OAuth2AuthorizationCodeBearer
import os
import datetime
import dotenv
from aiohttp import ClientSession
import hashlib

# load .env file
dotenv.load_dotenv()

app = FastAPI()

# Session management imports
from uuid import uuid4
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

# Constants and Application setup
CLIENT_ID = os.getenv("CLIENT_ID")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTHORITY = os.getenv("AUTHORITY")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY")
BACKEND_URL = os.getenv("BACKEND_URL")

logger = logging.getLogger(__name__)

app.mount("/public", StaticFiles(directory="/app/UI/public"), name="public")
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)

# Enable CORS (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{AUTHORITY}/oauth2/v2.0/authorize",
    tokenUrl=f"{AUTHORITY}/oauth2/v2.0/token",
    refreshUrl=f"{AUTHORITY}/oauth2/v2.0/token",
    scopes={
        "openid": "Open ID",
        "profile": "Profile",
        "email": "Email",
        "User.Read": "Read user profile"
    },
)

# Session store (for demonstration purposes, use Redis or other in production)
session_store = {}

# Helper function to set a session
def set_session(response: Response, user_data: dict) -> str:
    session_token = str(uuid4())
    session_store[session_token] = user_data
    response.set_cookie(key="session_token", value=session_token, httponly=True, secure=True)
    return session_token

# Helper function to get a session
def get_user_data_from_session(request: Request) -> Optional[dict]:
    session_token = request.cookies.get("session_token")
    return session_store.get(session_token)


# OAuth2 login and token endpoints
@app.get("/login")
async def login():
    return RedirectResponse(
        url=f"{AUTHORITY}/oauth2/v2.0/authorize"
            f"?client_id={CLIENT_ID}"
            f"&response_type=code"
            f"&redirect_uri={REDIRECT_URI}"
            f"&scope=openid profile email"
            f"&response_mode=query"
    )

@app.get("/token")
async def token(code: str, request: Request):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "openid profile email"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{AUTHORITY}/oauth2/v2.0/token", data=data, headers=headers) as resp:
            resp.raise_for_status()
            token_data = await resp.json()

            response = RedirectResponse(url="/dashboard")
            set_session(response, token_data) # Set session here
            return response
        

from jose import jwt, jwk


class User(BaseModel):
    sub: str = Field(alias="sub")  # Often 'sub' is used in JWT as the subject (user identifier)
    name: str
    email: str = ""  # Allow empty string for email

    class Config:
        schema_extra = {
            "example": {
                "sub": "1234567890",
                "name": "John Doe",
                "email": "john.doe@example.com"
            }
        }
        allow_population_by_field_name = True

class currentUser(BaseModel):
    id: int  # User ID
    name: str
    email: str

import aiohttp

@app.get("/user", response_model=currentUser)
async def get_user_info(request: Request):
    user_data = get_user_data_from_session(request)
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # Extract the id_token from the user data
    id_token = user_data.get("id_token")
    if not id_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing id_token")

    # Retrieve the signing keys from the OIDC discovery endpoint
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{AUTHORITY}/v2.0/.well-known/openid-configuration") as resp:
            oidc_config = await resp.json()
            jwks_uri = oidc_config["jwks_uri"]

        async with session.get(jwks_uri) as resp:
            jwks = await resp.json()

    # Find the signing key that matches the token's kid (key ID)
    token_headers = jwt.get_unverified_header(id_token)
    kid = token_headers["kid"]
    signing_key = None
    for key in jwks["keys"]:
        if key["kid"] == kid:
            signing_key = key
            break

    if not signing_key:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No matching signing key found")

    # Decode the id_token using the signing key
    try:
        decoded_token = jwt.decode(id_token, key=signing_key, algorithms=["RS256"], audience=CLIENT_ID)
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid id_token")

    # Extract the user information from the decoded token
    user_id = decoded_token.get("sub")
    user_name = decoded_token.get("name")
    user_email = decoded_token.get("email")

    # Create a User object with the retrieved information
    user_uuid = int(hashlib.sha1(user_id.encode("utf-8")).hexdigest(), 16) % (10 ** 8)
    user = currentUser(id=user_uuid, name=user_name, email=user_email)

    # URL to your backend endpoint that will receive this user data
    register_user_url = f"{BACKEND_URL}/users/"  # Update the URL to include the trailing slash
    backend_url = f"{BACKEND_URL}/user"

    # Sending the user data to the backend
    async with ClientSession() as session:
        headers = {'Content-Type': 'application/json'}
        user_create_data = {"email": user.email, "password": "dummypassword", "first_name": user_name.split()[0], "last_name": user_name.split()[1]}  # Include the required fields
        response = await session.post(backend_url, json=user.dict(), headers=headers)
        if response.status != 201:
            raise HTTPException(status_code=response.status, detail="Backend failed to process the data")
        response = await session.post(register_user_url, json=user_create_data, headers=headers)
        if response.status != 200:
            # if user already exists then move on
            if response.status == 400:
                print("User already exists")

    return user

# Secure endpoint example
@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    user_data = get_user_data_from_session(request)
    if not user_data:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    print(user_data)
    return FileResponse('/app/UI/private/dashboard.html')

@app.get("/js/dashboard", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    user_data = get_user_data_from_session(request)
    if not user_data:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return FileResponse('/app/UI/private/js/dashboard.js')

@app.get("/js/creator", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    user_data = get_user_data_from_session(request)
    if not user_data:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return FileResponse('/app/UI/private/js/creator.js')

@app.get("/js/script", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    user_data = get_user_data_from_session(request)
    if not user_data:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return FileResponse('/app/UI/private/js/script.js')

@app.get("/js/jspdf", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    user_data = get_user_data_from_session(request)
    if not user_data:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return FileResponse('/app/UI/private/js/jspdf.js')

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return FileResponse('/app/UI/public/login.html')

@app.get("/styles/login", response_class=HTMLResponse)
async def read_css(request: Request):
    return FileResponse('/app/UI/public/css/styles.css')

@app.get("/styles/dashboard", response_class=HTMLResponse)
async def read_css(request: Request):
    user_data = get_user_data_from_session(request)
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return FileResponse('/app/UI/private/css/styles.css')

@app.get("/styles/creator", response_class=HTMLResponse)
async def read_css(request: Request):
    user_data = get_user_data_from_session(request)
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return FileResponse('/app/UI/private/css/creator.css')

@app.get("/images/{path}", response_class=HTMLResponse)
async def read_css(request: Request, path: str):
    user_data = get_user_data_from_session(request)
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return FileResponse(f'/app/UI/private/images/{path}')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80, log_level="info", reload=True)