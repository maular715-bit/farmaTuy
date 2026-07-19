import os
from dotenv import load_dotenv
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
load_dotenv()

Base = declarative_base()
def get_database_url() -> str:
    
    url = os.getenv("DATABASE_URL")
    if url:
        return url

    # Valores para PostgreSQL
    driver = os.getenv("DB_DRIVER", "postgresql+psycopg2") 
    

    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "")
    host = os.getenv("DB_HOST", "postgres")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "postgres")
    return f"{driver}://{user}:{password}@{host}:{port}/{name}"

ENGINE = create_engine(
    get_database_url(),
    future=True,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=ENGINE, autoflush=False, autocommit=False, expire_on_commit=False, class_=Session)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=ENGINE)


