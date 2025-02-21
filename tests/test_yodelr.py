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


def test_add_post(
    yodelr: Yodelr,
    user_name: str,
    sample_10_posts: list[str],
):
    yodelr.add_post(user_name, sample_10_posts[0], 1)
    assert yodelr._is_post_in_system(user_name, sample_10_posts[0])


def test_delete_user_with_zero_post(
    yodelr: Yodelr, user_name: str, sample_10_posts: list[str]
):
    yodelr.add_user("u1")
    yodelr.add_user("u2")
    yodelr.add_user(user_name)
    yodelr.add_user("u3")
    yodelr.add_user("u4")
    yodelr.delete_user(user_name)
    assert not yodelr._is_user_in_system(user_name)


def test_delete_user_with_single_post(
    yodelr: Yodelr,
    user_name: str,
    sample_10_posts: list[str],
):
    yodelr.add_user("u1")
    yodelr.add_user("u2")
    yodelr.add_user(user_name)
    yodelr.add_post(user_name, sample_10_posts[3], 1)
    yodelr.delete_user(user_name)
    assert not yodelr._is_user_in_system(user_name)


def test_get_posts_size_1_for_user(
    yodelr: Yodelr,
    user_name: str,
    sample_10_posts: list[str],
):
    yodelr.add_user(user_name)
    yodelr.add_post(user_name, sample_10_posts[4], 1)
    assert yodelr.get_posts_for_user(user_name) == [sample_10_posts[4]]


def test_get_posts_size_3_for_user(
    yodelr: Yodelr,
    user_name: str,
    sample_10_posts: list[str],
):
    yodelr.add_user("u1")
    yodelr.add_post("u1", sample_10_posts[0], 1)
    yodelr.add_user(user_name)
    yodelr.add_post(user_name, sample_10_posts[1], 10)
    yodelr.add_post(user_name, sample_10_posts[2], 20)
    yodelr.add_post(user_name, sample_10_posts[3], 30)
    assert yodelr.get_posts_for_user(user_name) == sample_10_posts[1:4]
