import pytest
import v1
from yodelr import Yodelr


@pytest.fixture
def yodelr() -> Yodelr:
    return v1.YodelrV1()


def test_add_user(yodelr, user):
    yodelr.add_user(user)
    assert yodelr._is_user_in_system(user)
