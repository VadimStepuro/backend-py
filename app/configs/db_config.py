from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
import os

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1111@localhost:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
