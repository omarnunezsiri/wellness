"""Unit tests for configuration management."""

from unittest.mock import patch

import pytest

from backend.config import Settings, get_env_bool, get_env_int, get_env_str


class TestEnvironmentFunctions:
    """Test environment variable helper functions."""

    def test_get_env_str_success(self):
        """Test successful string environment variable retrieval."""
        # Arrange
        expected_value = "test_value"

        # Act
        with patch("os.getenv", return_value=expected_value):
            result = get_env_str("TEST_VAR")

        # Assert
        assert result == expected_value

    def test_get_env_str_missing(self):
        """Test error when string environment variable is missing."""
        # Arrange
        expected_error = "TEST_VAR environment variable is required"

        # Act & Assert
        with patch("os.getenv", return_value=None):
            with pytest.raises(ValueError, match=expected_error):
                get_env_str("TEST_VAR")

    def test_get_env_int_success(self):
        """Test successful integer environment variable retrieval."""
        # Arrange
        env_value = "42"
        expected_result = 42

        # Act
        with patch("os.getenv", return_value=env_value):
            result = get_env_int("TEST_VAR")

        # Assert
        assert result == expected_result

    def test_get_env_int_invalid(self):
        """Test error when integer environment variable is invalid."""
        # Arrange
        invalid_value = "not_a_number"
        expected_error = "TEST_VAR must be a valid integer"

        # Act & Assert
        with patch("os.getenv", return_value=invalid_value):
            with pytest.raises(ValueError, match=expected_error):
                get_env_int("TEST_VAR")

    def test_get_env_bool_true(self):
        """Test boolean environment variable parsing for true values."""
        # Arrange
        env_value = "true"
        expected_result = True

        # Act
        with patch("os.getenv", return_value=env_value):
            result = get_env_bool("TEST_VAR")

        # Assert
        assert result is expected_result

    def test_get_env_bool_false(self):
        """Test boolean environment variable parsing for false values."""
        # Arrange
        env_value = "false"
        expected_result = False

        # Act
        with patch("os.getenv", return_value=env_value):
            result = get_env_bool("TEST_VAR")

        # Assert
        assert result is expected_result

    def test_get_env_bool_case_insensitive(self):
        """Test boolean environment variable parsing is case insensitive."""
        # Arrange
        env_value = "TRUE"
        expected_result = True

        # Act
        with patch("os.getenv", return_value=env_value):
            result = get_env_bool("TEST_VAR")

        # Assert
        assert result is expected_result


@pytest.mark.unit
class TestSettings:
    """Test Settings class initialization."""

    @patch.dict(
        "os.environ",
        {
            "DATABASE_URL": "sqlite:///test.db",
            "HOST": "127.0.0.1",
            "PORT": "8000",
            "DEBUG": "true",
            "CORS_ORIGINS": '["http://localhost:3000"]',
            "SECRET_KEY": "test-key",
            "DEFAULT_USER_ID": "test_user",
            "GEMINI_API_KEY": "test-api-key",
        },
    )
    def test_settings_initialization(self):
        """Test Settings class initializes correctly with environment variables."""
        # Arrange
        expected_values = {
            "database_url": "sqlite:///test.db",
            "host": "127.0.0.1",
            "port": 8000,
            "debug": True,
            "cors_origins": ["http://localhost:3000"],
            "secret_key": "test-key",
            "default_user_id": "test_user",
            "gemini_api_key": "test-api-key",
        }

        # Act
        settings = Settings()

        # Assert
        assert settings.database_url == expected_values["database_url"]
        assert settings.host == expected_values["host"]
        assert settings.port == expected_values["port"]
        assert settings.debug is expected_values["debug"]
        assert settings.cors_origins == expected_values["cors_origins"]
        assert settings.secret_key == expected_values["secret_key"]
        assert settings.default_user_id == expected_values["default_user_id"]
        assert settings.gemini_api_key == expected_values["gemini_api_key"]

    @patch.dict(
        "os.environ",
        {
            "DATABASE_URL": "sqlite:///test.db",
            "HOST": "127.0.0.1",
            "PORT": "8000",
            "DEBUG": "true",
            "CORS_ORIGINS": "http://localhost:3000,http://127.0.0.1:3000",
            "SECRET_KEY": "test-key",
            "DEFAULT_USER_ID": "test_user",
            "GEMINI_API_KEY": "test-api-key",
        },
    )
    def test_cors_origins_comma_separated(self):
        """Test CORS origins parsing from comma-separated string."""
        # Arrange
        expected_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

        # Act
        settings = Settings()

        # Assert
        assert settings.cors_origins == expected_origins
