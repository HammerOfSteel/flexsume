# Start from the latest Alpine image
FROM alpine:latest

# Install Python, pip, and necessary build dependencies
RUN apk add --update python3 py3-pip \
    && apk add build-base python3-dev libffi-dev openssl-dev

# Set up a virtual environment
RUN python3 -m venv /venv
# Ensure that we use the virtual environment for our Python operations
ENV PATH="/venv/bin:$PATH"

# Install your required Python packages using pip in the virtual environment
RUN pip install fastapi uvicorn python-multipart aiofiles jinja2 itsdangerous \
    && pip install pydantic[dotenv] \
    && pip install httpx \
    && pip install "uvicorn[standard]" \
    && pip install pyOpenSSL \
    && pip install cryptography \
    && pip install python-jose[cryptography] \
    && pip install requests \
    && pip install urllib3 \
    && pip install python-jose \
    && pip install fastapi-microsoft-identity \
    && pip install fastapi-azure-auth \
    && pip install fastapi-sso \
    && pip install python-dotenv \
    && pip install aiohttp \
    && pip install aiohttp_session \
    && pip install asyncpg

# Create a directory for your application
WORKDIR /app

# Copy your Python script and any necessary files into the Docker image
COPY /frontend/ /app/

# Expose the port your app runs on
EXPOSE 80

# Set the working directory
WORKDIR /app

# Set the command to run your Python script with Uvicorn
# Note: Adjust the command to ensure it's executed within the virtual environment
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
