from datetime import timedelta, datetime

from fastapi.security import OAuth2PasswordBearer
import jwt
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

load_dotenv()

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

secret_key = os.getenv("SECRET_KEY")
seconds_expiration = os.getenv("SECONDS_EXPIRATION")


def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


def hash_password(password: str):
    return password_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(seconds=int(seconds_expiration))

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")
    return encoded_jwt