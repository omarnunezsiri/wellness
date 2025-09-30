import hashlib
from datetime import UTC, datetime, timedelta
from typing import cast

from sqlalchemy.orm import Session

from .database import OTP, get_settings

settings = get_settings()


def generate_otp(uuid: str, validity_period: int, timestamp: datetime, salt: str = settings.secret_key) -> str:
    """
    Generate a time-based one-time password (OTP) using SHA-256.

    Args:
        uuid (str): The user's unique identifier.
        timestamp (datetime): The current timestamp for OTP generation.
        salt (str): A secret key used as a salt for hashing.
        validity_period (int): The validity period of the OTP in minutes.

    Returns:
        str: The generated OTP as a SHA-256 hash.
    """

    if not uuid:
        raise ValueError("uuid is required for otp generation")

    # Round timestamp to the nearest validity_period minutes for time-based OTPs
    time_window = timestamp - timedelta(
        minutes=timestamp.minute % validity_period, seconds=timestamp.second, microseconds=timestamp.microsecond
    )

    # Combine salt, UUID, and time window
    raw_input = f"{salt}{uuid}{time_window.isoformat()}"
    return hashlib.sha256(raw_input.encode()).hexdigest()


def generate_and_store_otp(uuid: str, db_session: Session, validity_period: int = 15) -> str:
    """
    Generate and store an OTP with an expiry time.

    Args:
        uuid (str): The user's unique identifier.
        db_session: The database session for storing the OTP.
        validity_period (int): The validity period of the OTP in minutes.

    Returns:
        str: The generated OTP.
    """

    otp = generate_otp(uuid, validity_period=validity_period, timestamp=datetime.now(UTC))

    # Store OTP in lowercase for consistent case-insensitive validation
    otp_normalized = otp.lower()
    otp_entry = OTP(otp=otp_normalized, uuid=uuid, validity_period=validity_period)
    db_session.add(otp_entry)
    db_session.commit()
    return otp


def validate_otp(uuid: str, otp: str, db_session: Session) -> bool:
    """
    Validate an OTP by checking its value and expiry time.

    Args:
        uuid (str): The user's unique identifier.
        otp (str): The OTP to validate.
        db_session: The database session for querying.

    Returns:
        bool: True if the OTP is valid, False otherwise.
    """

    # Normalize OTP to lowercase for case-insensitive comparison
    otp_normalized = otp.lower().strip()
    otp_entry = db_session.query(OTP).filter_by(otp=otp_normalized, uuid=uuid).first()
    if otp_entry is None:
        return False

    # Check if the OTP is expired
    current_time = datetime.now(UTC)
    created_at = otp_entry.created_at

    # Given SQLite constraints, datetimes are stored as naive. Ensures UTC timezone
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=UTC)

    validity_period = cast(int, otp_entry.validity_period)
    if (current_time - created_at).total_seconds() > validity_period * 60:
        return False

    return True
