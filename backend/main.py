import uuid
from datetime import datetime
from html import escape

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.config import get_settings
from backend.database import Affirmation, DailyTask, SessionLocal, User, get_db
from backend.task_ai import TaskAI

settings = get_settings()

app = FastAPI(
    title="Daily Wellness Tracker API",
    description="A mindful productivity app with daily affirmations and task management",
    version="1.0.0",
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

DB_DEPENDENCY = Depends(get_db)
task_ai = TaskAI(settings.gemini_api_key)


class TaskCreate(BaseModel):
    task_text: str
    user_id: str = settings.default_user_id

    @field_validator("task_text")
    @classmethod
    def validate_task_text(cls, v):
        """Validate task text length to match frontend validation (3-100 characters)."""
        if not v or not v.strip():
            raise ValueError("Task text cannot be empty")

        v = v.strip()
        v = escape(v)

        if len(v) < 3:
            raise ValueError("Task text must be at least 3 characters long")
        if len(v) > 100:
            raise ValueError("Task text must be less than 100 characters long")

        return v


class TaskUpdate(BaseModel):
    completed: bool
    user_id: str


def add_sample_affirmations():
    """Populates the database with sample affirmations if none exist."""
    with SessionLocal() as db:
        if db.query(Affirmation).count() == 0:
            sample_affirmations = [
                "You are capable of amazing things.",
                "Today is filled with positive opportunities.",
                "You have the power to create change.",
                "Believe in yourself and all that you are.",
                "Your potential is limitless.",
                "You are worthy of love and respect.",
                "Embrace the glorious mess that you are.",
                "You are enough, just as you are.",
                "Your life is filled with purpose.",
                "You are resilient, strong, and brave.",
            ]

            for affirmation in sample_affirmations:
                db.add(Affirmation(text=affirmation))

            db.commit()


add_sample_affirmations()


def validate_user_id(user_id: str, db: Session) -> bool:
    """Validate that a user_id exists in the database."""
    user = db.query(User).filter(User.user_id == user_id).first()
    return user is not None


@app.post("/api/users")
def create_user(db: Session = DB_DEPENDENCY):
    """Creates a new user with a unique UUID."""
    user_id = str(uuid.uuid4())

    new_user = User(user_id=user_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"user_id": user_id}


@app.get("/")
def read_root():
    return {"message": "Daily Wellness Tracker API"}


@app.get("/api/affirmations")
def get_random_affirmation(db: Session = DB_DEPENDENCY):
    """Retrieves a random affirmation from the database."""
    affirmation = db.query(Affirmation).order_by(func.random()).first()
    if affirmation:
        return {"id": affirmation.id, "text": affirmation.text}
    else:
        return {"id": 0, "text": "You are amazing just as you are."}


@app.get("/api/daily-data")
def get_daily_data(date: str = "", user_id: str = "", db: Session = DB_DEPENDENCY):
    """Fetches daily data including an affirmation and tasks for a specific date and user."""
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")

    if not validate_user_id(user_id, db):
        raise HTTPException(status_code=401, detail="Invalid user_id")

    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    affirmation = db.query(Affirmation).order_by(func.random()).first()
    tasks = db.query(DailyTask).filter(DailyTask.created_date == date, DailyTask.user_id == user_id).all()

    return {
        "date": date,
        "affirmation": affirmation.text if affirmation else "You are amazing just as you are.",
        "tasks": [{"id": task.id, "description": task.task_text, "completed": task.completed} for task in tasks],
    }


@app.post("/api/tasks")
def create_task(task_data: TaskCreate, date: str = "", db: Session = DB_DEPENDENCY):
    """Creates a new task for a given date and user."""
    if not validate_user_id(task_data.user_id, db):
        raise HTTPException(status_code=401, detail="Invalid user_id")

    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    new_task = DailyTask(task_text=task_data.task_text, created_date=date, user_id=task_data.user_id, completed=False)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {"id": new_task.id, "description": new_task.task_text, "completed": new_task.completed}


@app.put("/api/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate, db: Session = DB_DEPENDENCY):
    """Updates the completion status of a task."""
    if not validate_user_id(task_update.user_id, db):
        raise HTTPException(status_code=401, detail="Invalid user_id")

    task = db.query(DailyTask).filter(DailyTask.id == task_id, DailyTask.user_id == task_update.user_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found or access denied")

    # Maintain consistency with dynamic attribute updates
    setattr(task, "completed", task_update.completed)
    db.commit()

    return {"id": task.id, "description": task.task_text, "completed": task.completed}


@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int, user_id: str = "", db: Session = DB_DEPENDENCY):
    """Deletes a task from the database."""
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")

    if not validate_user_id(user_id, db):
        raise HTTPException(status_code=401, detail="Invalid user_id")

    task = db.query(DailyTask).filter(DailyTask.id == task_id, DailyTask.user_id == user_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found or access denied")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}


@app.post("/api/celebrate-task")
def celebrate_task(task: dict):
    """Endpoint to celebrate task completion using AI-generated messages."""
    completed_task = task.get("completed_task")

    if not completed_task:
        raise HTTPException(status_code=400, detail="completed_task is required")

    celebration_message = task_ai.celebrate_task_completion(completed_task)
    return {"message": celebration_message}


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host=settings.host, port=settings.port, reload=settings.debug, server_header=False)
