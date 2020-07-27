import sys

sys.path.append("..")
from passlib.context import CryptContext
from models.jwt_user import JWTUser
from datetime import datetime, timedelta
from utils.const import JWT_EXPIRATION_TIME_MINUTES, JWT_SECRET_KEY, JWT_ALGORITHM
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_401_UNAUTHORIZED
import time


pwd_context = CryptContext(schemes=["bcrypt"])
oauth_schema = OAuth2PasswordBearer(tokenUrl="/token")
jwt_user = {
    "username": "user1",
    "password": "$2b$12$yWgvi0KN7zasAvrGSgHqnutEmju7RbnSQLpN3KDhUAqU68ccC8k1K",
    "disabled": False,
    "role": "admin",
}
database_jwt_user = JWTUser(**jwt_user)


def get_hashed_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        return e

# Authenticate & give JWT token
def authenticate_user(user: JWTUser):
    try:
        if database_jwt_user.username == user.username:
            if verify_password(user.password, database_jwt_user.password):
                user.role = "admin"
                return user
            return None
    except Exception as e:
        return e


# Create JWT token
def create_jwt_token(user: JWTUser):
    try:
        expiration = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
        jwt_payload = {"sub": user.username, "role": user.role, "exp": expiration}
        jwt_token = jwt.encode(jwt_payload, JWT_SECRET_KEY, JWT_ALGORITHM)
        return jwt_token
    except Exception as e:
        return e

# Check if JWT token is valid
def check_jwt_token(token: str):
    try:
        jwt_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        username = jwt_payload.get("sub")
        role = jwt_payload.get("role")
        expiration = jwt_payload.get("exp")
        if time.time() < expiration:
            if database_jwt_user.username == username:
                return final_checks(role)
    except:
        return False
    return False
    


# Last check & return result
def final_checks(role:str):
    if role == "admin":
        return True
    else:
        return False
    
