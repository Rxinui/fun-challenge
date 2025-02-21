import pytest
import v1
import time


@pytest.fixture
def post_single_topic(username) -> str:
    return "This is a #message, with a topic."


@pytest.fixture
def post_multiple_topics(username) -> str:
    return "This has #message with #multiple a #topic."


@pytest.fixture
def post_no_topic(username) -> str:
    return "This has no topic!"


def test_get_topic(post_single_topic):
    assert v1.YodelrV1._extract_topics(post_single_topic) == ["message"]


def test_get_topics(post_multiple_topics):
    assert v1.YodelrV1._extract_topics(post_multiple_topics) == [
        "message",
        "multiple",
        "topic",
    ]


def test_get_no_topic(post_no_topic):
    assert v1.YodelrV1._extract_topics(post_no_topic) == []
