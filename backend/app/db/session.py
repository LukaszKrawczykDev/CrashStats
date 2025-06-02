from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection
from app.database import DATABASE_URL  # lub z configu, jeśli masz

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_isolated_session(level: str = "REPEATABLE READ") -> Session:
    connection: Connection = engine.connect()
    connection.execution_options(isolation_level=level)
    return Session(bind=connection)