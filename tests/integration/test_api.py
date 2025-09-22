"""Integration tests for API endpoints."""

import pytest

from backend.database import Affirmation, DailyTask


@pytest.mark.integration
class TestAffirmationsAPI:
    """Test affirmations API endpoints."""

    def test_get_random_affirmation_with_data(self, client, test_db):
        """Test getting random affirmation when database has data."""
        # Arrange
        test_affirmation_text = "Test affirmation"
        db = test_db()
        affirmation = Affirmation(text=test_affirmation_text)
        db.add(affirmation)
        db.commit()
        db.close()

        # Act
        response = client.get("/api/affirmations")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "text" in data
        assert data["text"] == test_affirmation_text

    def test_get_random_affirmation_empty_database(self, client, test_db):
        """Test getting random affirmation when database is empty."""
        # Arrange
        expected_fallback = "You are amazing just as you are."

        # Act
        response = client.get("/api/affirmations")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 0
        assert data["text"] == expected_fallback


@pytest.mark.integration
class TestTasksAPI:
    """Test tasks API endpoints."""

    def test_create_task_success(self, client, test_user):
        """Test successful task creation."""
        # Arrange
        user_id = test_user
        task_data = {"task_text": "Test task", "user_id": user_id}
        test_date = "2024-01-01"

        # Act
        response = client.post(f"/api/tasks?date={test_date}", json=task_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "Test task"
        assert data["completed"] is False
        assert "id" in data

    def test_create_task_validation_too_short(self, client, test_user):
        """Test task creation with text too short."""
        # Arrange
        user_id = test_user
        task_data = {
            "task_text": "Hi",  # Only 2 characters
            "user_id": user_id,
        }

        # Act
        response = client.post("/api/tasks", json=task_data)

        # Assert
        assert response.status_code == 422

    def test_create_task_validation_too_long(self, client, test_user):
        """Test task creation with text too long."""
        # Arrange
        user_id = test_user
        task_data = {
            "task_text": "a" * 101,  # 101 characters
            "user_id": user_id,
        }

        # Act
        response = client.post("/api/tasks", json=task_data)

        # Assert
        assert response.status_code == 422

    def test_update_task_completion(self, client, test_db, test_user):
        """Test updating task completion status."""
        # Arrange
        user_id = test_user
        db = test_db()
        task = DailyTask(task_text="Test task", created_date="2024-01-01", user_id=user_id, completed=False)
        db.add(task)
        db.commit()
        db.refresh(task)
        task_id = task.id
        db.close()

        update_data = {"completed": True, "user_id": user_id}

        # Act
        response = client.put(f"/api/tasks/{task_id}", json=update_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True

    def test_update_task_not_found(self, client, test_user):
        """Test updating non-existent task."""
        # Arrange
        user_id = test_user
        non_existent_task_id = 999
        update_data = {"completed": True, "user_id": user_id}

        # Act
        response = client.put(f"/api/tasks/{non_existent_task_id}", json=update_data)

        # Assert
        assert response.status_code == 404

    def test_delete_task_success(self, client, test_db, test_user):
        """Test successful task deletion."""
        # Arrange
        user_id = test_user
        db = test_db()
        task = DailyTask(task_text="Test task", created_date="2024-01-01", user_id=user_id, completed=False)
        db.add(task)
        db.commit()
        db.refresh(task)
        task_id = task.id
        db.close()

        # Act
        response = client.delete(f"/api/tasks/{task_id}?user_id={user_id}")

        # Assert
        assert response.status_code == 200
        assert "Task deleted successfully" in response.json()["message"]

    def test_delete_task_not_found(self, client, test_user):
        """Test deleting non-existent task."""
        # Arrange
        user_id = test_user
        non_existent_task_id = 999

        # Act
        response = client.delete(f"/api/tasks/{non_existent_task_id}?user_id={user_id}")

        # Assert
        assert response.status_code == 404

    def test_get_daily_data(self, client, test_db, test_user):
        """Test getting daily data with affirmation and tasks."""
        # Arrange
        user_id = test_user
        db = test_db()
        test_date = "2024-01-01"

        # Add affirmation
        affirmation = Affirmation(text="Daily test affirmation")
        db.add(affirmation)

        # Add tasks
        task1 = DailyTask(task_text="Task 1", created_date=test_date, user_id=user_id, completed=False)
        task2 = DailyTask(task_text="Task 2", created_date=test_date, user_id=user_id, completed=True)
        db.add(task1)
        db.add(task2)
        db.commit()
        db.close()

        # Act
        response = client.get(f"/api/daily-data?date={test_date}&user_id={user_id}")

        # Assert
        assert response.status_code == 200
        data = response.json()

        assert data["date"] == test_date
        assert data["affirmation"] == "Daily test affirmation"
        assert len(data["tasks"]) == 2
        assert any(task["description"] == "Task 1" for task in data["tasks"])
        assert any(task["description"] == "Task 2" for task in data["tasks"])


@pytest.mark.integration
class TestCelebrateTaskAPI:
    """Test task celebration API."""

    def test_celebrate_task_success(self, client):
        """Test successful task celebration."""
        # Arrange
        from unittest.mock import patch

        completed_task = "Drink water"
        expected_message = "Great job! 🌟"
        request_data = {"completed_task": completed_task}

        # Act
        with patch("backend.main.task_ai") as mock_task_ai:
            mock_task_ai.celebrate_task_completion.return_value = expected_message
            response = client.post("/api/celebrate-task", json=request_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == expected_message
        mock_task_ai.celebrate_task_completion.assert_called_once_with(completed_task)

    def test_celebrate_task_missing_task(self, client):
        """Test task celebration with missing completed_task."""
        # Arrange
        empty_request = {}

        # Act
        response = client.post("/api/celebrate-task", json=empty_request)

        # Assert
        assert response.status_code == 400
        assert "completed_task is required" in response.json()["detail"]


@pytest.mark.integration
class TestRootAPI:
    """Test root API endpoint."""

    def test_root_endpoint(self, client):
        """Test root endpoint returns welcome message."""
        # Arrange
        expected_message = "Daily Wellness Tracker API"

        # Act
        response = client.get("/")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == expected_message


@pytest.mark.integration
class TestUsersAPI:
    """Test users API endpoints."""

    def test_create_user(self, client):
        """Test creating a user via the API."""
        # Act
        response = client.post("/api/users")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
