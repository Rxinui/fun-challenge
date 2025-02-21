import pytest
import v1
import time
from yodelr import Yodelr


@pytest.fixture
def yodelr() -> Yodelr:
    return v1.YodelrV1()


def test_add_user(yodelr: Yodelr, username: str):
    yodelr.add_user(username)
    assert yodelr._is_user_in_system(username)


def test_add_post(yodelr: Yodelr, username):
    post_text = "My very #first #test post."
    yodelr.add_post(username, post_text, str(int(time.time())))
    assert yodelr._is_post_in_system(username, post_text)
