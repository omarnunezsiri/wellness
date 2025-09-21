"""
Pytest configuration and shared fixtures for the test suite.
"""

import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database import Base, get_db
from backend.main import app


@pytest.fixture(scope="session")
def test_env():
    """Set up test environment variables."""
    test_env_vars = {
        "DATABASE_URL": "sqlite:///./test.db",
        "HOST": "127.0.0.1",
        "PORT": "8000",
        "DEBUG": "true",
        "CORS_ORIGINS": '["http://localhost:3000"]',
        "FRONTEND_DIR": "./frontend/dist",
        "STATIC_DIR": "./frontend/dist/assets",
        "SECRET_KEY": "test-secret-key-123",
        "DEFAULT_USER_ID": "test_user",
        "GEMINI_API_KEY": "test-api-key",
    }

    # Set test environment variables
    for key, value in test_env_vars.items():
        os.environ[key] = value

    yield test_env_vars

    # Clean up test database file with retry logic
    for attempt in range(3):
        try:
            if os.path.exists("test.db"):
                os.remove("test.db")
                print("✓ Test database cleaned up successfully")
                break
        except PermissionError:
            if attempt < 2:
                import time

                time.sleep(0.1)
                continue
            else:
                print("Test database cleanup skipped (file locked)")
        except Exception as e:
            print(f"Test database cleanup failed: {e}")
            break


@pytest.fixture(scope="function")
def test_db(test_env):
    """Create a test database session."""
    engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create all tables
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestingSessionLocal

    # Close engine and clear overrides
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def client(test_db):
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def sample_affirmations():
    """Sample affirmations for testing."""
    return [
        "You are capable of amazing things.",
        "Today is filled with positive opportunities.",
        "You have the power to create change.",
    ]


@pytest.fixture
def sample_tasks():
    """Sample tasks for testing."""
    return [
        {"task_text": "Drink 8 glasses of water", "completed": False},
        {"task_text": "Go for a 30-minute walk", "completed": True},
        {"task_text": "Practice meditation", "completed": False},
    ]
