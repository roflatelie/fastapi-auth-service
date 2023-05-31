import pytest as pytest
from src.usecases.password_hash import get_password_hash, verify_password


def test_password_hash():
    password = "test_password"
    hashed_password = get_password_hash(password)

    assert verify_password(password, hashed_password)
