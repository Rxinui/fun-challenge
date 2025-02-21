import pytest


@pytest.fixture(scope="module")
def user_name() -> str:
    return "Rxinui"
