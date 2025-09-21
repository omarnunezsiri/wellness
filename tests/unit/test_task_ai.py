"""Unit tests for TaskAI functionality."""

from unittest.mock import Mock, patch

import pytest

from backend.task_ai import TaskAI


@pytest.mark.unit
class TestTaskAI:
    """Test TaskAI class functionality."""

    def test_init(self):
        """Test TaskAI initialization."""
        # Arrange
        test_api_key = "test-api-key"

        # Act
        with patch("backend.task_ai.genai.Client") as mock_client:
            task_ai = TaskAI(test_api_key)

        # Assert
        mock_client.assert_called_once_with(api_key=test_api_key)
        assert task_ai.model == "gemini-2.0-flash-001"

    def test_celebrate_task_completion_empty_task(self):
        """Test celebration with empty task returns fallback."""
        # Arrange
        empty_task = ""
        expected_fallback = "Great job completing your task! You're taking wonderful care of yourself. 🌟"

        # Act
        with patch("backend.task_ai.genai.Client"):
            task_ai = TaskAI("test-api-key")
            result = task_ai.celebrate_task_completion(empty_task)

        # Assert
        assert expected_fallback in result
        assert "🌟" in result

    def test_celebrate_task_completion_success(self):
        """Test successful task celebration."""
        # Arrange
        task_description = "Complete morning routine"
        expected_response = "Amazing work on that task! 🍂✨"

        # Act
        with patch("backend.task_ai.genai.Client") as mock_client:
            mock_response = Mock()
            mock_response.text = expected_response
            mock_client.return_value.models.generate_content.return_value = mock_response

            task_ai = TaskAI("test-api-key")
            result = task_ai.celebrate_task_completion(task_description)

        # Assert
        assert result == expected_response

    def test_celebrate_task_completion_api_error(self):
        """Test task celebration with API error returns fallback."""
        # Arrange
        task_description = "Complete morning routine"

        # Act
        with patch("backend.task_ai.genai.Client") as mock_client:
            mock_client.return_value.models.generate_content.side_effect = Exception("API Error")

            task_ai = TaskAI("test-api-key")
            result = task_ai.celebrate_task_completion(task_description)

        # Assert
        assert "Beautiful work completing 'Complete morning routine'!" in result
        assert "🌟" in result

    def test_celebrate_task_completion_sanitizes_input(self):
        """Test that task input is properly sanitized."""
        # Arrange
        malicious_input = "<script>alert('test')</script>"

        # Act
        with patch("backend.task_ai.genai.Client") as mock_client:
            mock_response = Mock()
            mock_response.text = "Great job! 🌟"
            mock_client.return_value.models.generate_content.return_value = mock_response

            task_ai = TaskAI("test-api-key")
            result = task_ai.celebrate_task_completion(malicious_input)

        # Assert
        mock_client.return_value.models.generate_content.assert_called_once()
        args = mock_client.return_value.models.generate_content.call_args[1]["contents"]
        assert result == "Great job! 🌟"
        assert "&lt;script&gt;" in args  # HTML should be escaped

    def test_fallback_message(self):
        """Test fallback message generation."""
        # Arrange
        task_description = "Test task"
        expected_message = "Beautiful work completing 'Test task'! You're taking such good care of yourself. 🌟"

        # Act
        with patch("backend.task_ai.genai.Client"):
            task_ai = TaskAI("test-api-key")
            result = task_ai._get_fallback_message(task_description)

        # Assert
        assert result == expected_message
