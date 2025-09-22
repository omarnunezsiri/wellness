"""
Database models and configuration for the Daily Wellness Tracker application.

This module defines SQLAlchemy models for storing affirmations and daily tasks,
along with database session management and connection setup.
"""

from datetime import UTC, datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import get_settings

settings = get_settings()
database_url = settings.database_url

engine = create_engine(
    database_url,
    connect_args={"check_same_thread": False} if database_url.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    """
    Model for storing user information.

    This table tracks registered users with their unique identifiers
    and creation timestamps for proper user management and validation.

    Attributes:
        id: Primary key, auto-incrementing integer identifier
        user_id: Unique UUID string identifier for the user
        created_at: Timestamp when the user was created
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


class Affirmation(Base):
    """
    Model for storing motivational affirmations.

    This table contains positive affirmation messages that are randomly
    displayed to users to provide daily motivation and encouragement.

    Attributes:
        id: Primary key, auto-incrementing integer identifier
        category: Optional category for grouping affirmations (e.g., 'motivation', 'self-care')
        text: The actual affirmation text content displayed to users
    """

    __tablename__ = "affirmations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category = Column(String, index=True)
    text = Column(Text, index=True)


class DailyTask(Base):
    """
    Model for storing user daily tasks and their completion status.

    This table tracks tasks that users want to accomplish on specific dates,
    including their completion status and associated user information.

    Attributes:
        id: Primary key, auto-incrementing integer identifier
        task_text: The description of the task to be completed
        completed: Boolean flag indicating if the task has been completed
        created_date: Date when the task was created (YYYY-MM-DD format)
        user_id: Identifier for the user who owns this task
    """

    __tablename__ = "daily_tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    task_text = Column(Text, nullable=False)
    completed = Column(Boolean, default=False)
    created_date = Column(String, index=True)
    user_id = Column(String, default="default_user", index=True)


Base.metadata.create_all(bind=engine)


def get_db():
    """
    Database dependency for FastAPI endpoints.

    This function provides a database session for each request and ensures
    proper cleanup after the request is completed. Used as a dependency
    injection in FastAPI route handlers.

    Yields:
        Session: SQLAlchemy database session for database operations

    Example:
        @app.get("/api/tasks")
        def get_tasks(db: Session = Depends(get_db)):
            return db.query(DailyTask).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
