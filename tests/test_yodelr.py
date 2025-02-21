import pytest
import v1
import time
from yodelr import Yodelr


@pytest.fixture
def yodelr() -> Yodelr:
    return v1.YodelrV1()


def test_add_user(yodelr: Yodelr, user_name: str):
    yodelr.add_user(user_name)
    assert yodelr._is_user_in_system(user_name)


def test_add_post(yodelr: Yodelr, user_name):
    post_text = "My very #first #test post."
    yodelr.add_post(user_name, post_text, str(int(time.time())))
    assert yodelr._is_post_in_system(user_name, post_text)


def test_delete_user_with_zero_post(yodelr: Yodelr, user_name: str):
    yodelr.add_user("u1")
    yodelr.add_user("u2")
    yodelr.add_user(user_name)
    yodelr.add_user("u3")
    yodelr.add_user("u4")
    yodelr.delete_user(user_name)
    assert not yodelr._is_user_in_system(user_name)


def test_delete_user_with_single_post(yodelr: Yodelr, user_name: str):
    yodelr.add_user("u1")
    yodelr.add_user("u2")
    yodelr.add_user(user_name)
    yodelr.add_post(user_name, "Random #post for test", time.now())
    yodelr.delete_user(user_name)
    assert not yodelr._is_user_in_system(user_name)
