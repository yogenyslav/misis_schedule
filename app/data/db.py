from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeBase
from sqlalchemy import create_engine

from app.configs.settings import settings

engine = create_engine(str(settings.DATABASE_URI))
SessionLocal = sessionmaker(bind=engine, autoflush=True)

Base: DeclarativeBase = declarative_base()
