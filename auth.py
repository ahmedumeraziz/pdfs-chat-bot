import os
import time
from jose import jwt, JWTError
from passlib.context import CryptContext

# Use environment variables for secrets
SECRET_KEY = os.getenv("JWT_SECRET", "your_strong_secret")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Single user credentials (replace with your own)
USER_DATA = {
    "username": "admin",
    "password": pwd_context.hash("your_secure_password")
}

def authenticate(username: str, password: str):
    if username == USER_DATA["username"]:
        return pwd_context.verify(password, USER_DATA["password"])
    return False

def generate_token(username: str):
    payload = {
        "sub": username,
        "exp": time.time() + 3600  # 1 hour expiration
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"] == USER_DATA["username"]
    except JWTError:
        return False
