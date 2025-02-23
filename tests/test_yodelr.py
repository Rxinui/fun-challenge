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


def test_get_posts_size_0_for_user(
    yodelr: Yodelr,
    user_name: str,
    sample_10_posts: list[str],
):
    yodelr.add_user(user_name)
    assert yodelr.get_posts_for_user(user_name) == []


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
    """Do not test the order of the element (no sort)"""
    yodelr.add_user("u1")
    yodelr.add_post("u1", sample_10_posts[0], 1)
    yodelr.add_user(user_name)
    yodelr.add_post(user_name, sample_10_posts[1], 10)
    yodelr.add_post(user_name, sample_10_posts[2], 20)
    yodelr.add_post(user_name, sample_10_posts[3], 30)
    result = yodelr.get_posts_for_user(user_name)
    assert (
        result[0] in sample_10_posts[1:4]
        and result[1] in sample_10_posts[1:4]
        and result[2] in sample_10_posts[1:4]
    )


def test_get_posts_size_3_is_desc_sorted(
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
    assert yodelr.get_posts_for_user(user_name) == [
        sample_10_posts[3],
        sample_10_posts[2],
        sample_10_posts[1],
    ]


def test_get_posts_size_0_for_topic(
    yodelr: Yodelr, user_name: str, sample_10_posts_and_topics: list[tuple[str, list]]
):
    FIRST_TOPIC = 0
    POST = 0
    TOPICS = 1
    yodelr.add_user(user_name)
    yodelr.add_post(user_name, sample_10_posts_and_topics[1][POST], 1)
    yodelr.add_post(user_name, sample_10_posts_and_topics[3][POST], 2)
    yodelr.add_post(user_name, sample_10_posts_and_topics[9][POST], 5)
    assert yodelr.get_posts_for_topic("topic") == []


def test_get_posts_size_1_for_topic(
    yodelr: Yodelr, user_name: str, sample_10_posts_and_topics: list[tuple[str, list]]
):
    FIRST_TOPIC = 0
    POST = 0
    TOPICS = 1
    yodelr.add_user(user_name)
    yodelr.add_post(user_name, sample_10_posts_and_topics[4][POST], 1)
    assert yodelr.get_posts_for_topic(
        sample_10_posts_and_topics[4][TOPICS][FIRST_TOPIC]
    ) == [sample_10_posts_and_topics[4][POST]]


def test_get_posts_size_3_for_topic(
    yodelr: Yodelr, user_name: str, sample_10_posts_and_topics: list[tuple[str, list]]
):
    POST = 0
    yodelr.add_user(user_name)
    yodelr.add_post(user_name, sample_10_posts_and_topics[8][POST], 1)
    yodelr.add_post(user_name, sample_10_posts_and_topics[1][POST], 12)
    yodelr.add_post(user_name, sample_10_posts_and_topics[6][POST], 175)
    assert yodelr.get_posts_for_topic("topic") == [
        sample_10_posts_and_topics[6][POST],
        sample_10_posts_and_topics[8][POST],
    ]


def test_get_trending_topics_oldest_to_latest(
    yodelr: Yodelr, user_name: str, sample_10_posts: list[tuple[str, list]]
):
    OLDEST_TIMESTAMP = 0
    LATEST_TIMESTAMP = len(sample_10_posts) - 1
    for i in range(len(sample_10_posts)):
        yodelr.add_post(user_name, sample_10_posts[i], i)
    assert yodelr.get_trending_topics(OLDEST_TIMESTAMP, LATEST_TIMESTAMP) == [
        "post",
        "test",
        "topic",
        "first",
        "full",
    ]


def test_get_trending_topics_in_between_ts_count_focus(
    yodelr: Yodelr, user_name: str, sample_10_posts: list[tuple[str, list]]
):
    TS_1 = 1
    TS_2 = 6
    for i in range(len(sample_10_posts)):
        yodelr.add_post(user_name, sample_10_posts[i], i)
    assert yodelr.get_trending_topics(TS_1, TS_2) == ["post", "test", "topic"]


def test_get_trending_topics_in_between_ts_alphabetic_focus(
    yodelr: Yodelr, user_name: str, sample_10_posts: list[tuple[str, list]]
):
    TS_1 = 7
    TS_2 = 9
    for i in range(len(sample_10_posts)):
        yodelr.add_post(user_name, sample_10_posts[i], i)
    assert yodelr.get_trending_topics(TS_1, TS_2) == ["full", "topic"]
