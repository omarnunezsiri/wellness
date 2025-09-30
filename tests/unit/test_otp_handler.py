from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database import OTP, Base
from backend.otp_handler import generate_and_store_otp, generate_otp, validate_otp


@pytest.fixture(scope="function")
def db_session():
    # Setup in-memory SQLite database for testing
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


def test_generate_otp():
    # Arrange
    uuid = "123e4567-e89b-12d3-a456-426614174000"
    validity_period = 15
    timestamp = datetime.now(UTC)

    # Act
    otp = generate_otp(uuid, validity_period=validity_period, timestamp=timestamp)

    # Assert
    assert isinstance(otp, str)
    assert len(otp) == 64  # SHA-256 hash length

    # Ensure the same inputs produce the same OTP
    otp2 = generate_otp(uuid, validity_period=validity_period, timestamp=timestamp)
    assert otp == otp2


def test_generate_and_store_otp(db_session):
    # Arrange
    uuid = "123e4567-e89b-12d3-a456-426614174000"
    validity_period = 15

    # Act
    otp = generate_and_store_otp(uuid, db_session, validity_period=validity_period)
    otp_entry = db_session.query(OTP).filter_by(otp=otp, uuid=uuid).first()

    # Assert
    assert isinstance(otp, str)
    assert len(otp) == 64

    assert otp_entry is not None
    assert otp_entry.otp == otp
    assert otp_entry.uuid == uuid
    assert otp_entry.validity_period == validity_period


def test_validate_otp(db_session):
    # Arrange
    uuid = "123e4567-e89b-12d3-a456-426614174000"
    validity_period = 1  # 1 minute validity
    otp = generate_and_store_otp(uuid, db_session, validity_period=validity_period)

    # Act & Assert - Valid OTP
    assert validate_otp(uuid, otp, db_session) is True

    # Arrange - Simulate expiration by setting created_at to 2 minutes ago
    otp_entry = db_session.query(OTP).filter_by(otp=otp, uuid=uuid).first()
    otp_entry.created_at = datetime.now(UTC) - timedelta(minutes=2)
    db_session.commit()

    # Act & Assert - Expired OTP
    assert validate_otp(uuid, otp, db_session) is False
