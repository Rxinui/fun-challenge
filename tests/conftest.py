import pytest


@pytest.fixture(scope="module")
def username() -> str:
    return "Rxinui"
