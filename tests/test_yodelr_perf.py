import os
import pytest
import random
import v1
import logging
import math
from time import time
from lorem_text import lorem
from yodelr import Yodelr

ENV_PERF_SIZE = os.getenv("PERF_GENERATOR_SIZE")


def random_post_generator(words: int) -> str:
    post = ""
    for i in range(words):
        w = lorem.words(1)
        if random.randint(1, 6) in [2, 3]:
            w = "#" + w
        post += w + " "
    return post


@pytest.fixture
def yodelr() -> Yodelr:
    return v1.YodelrV1(fast_write=True)


@pytest.fixture
def user_names() -> list[str]:
    return ["u1", "u2", "u3"]


@pytest.fixture
def several_user_names() -> list[str]:
    return [f"u{i}" for i in range(100)]


@pytest.fixture()
def random_post_generator_words() -> str:
    """_summary_

    Returns:
        str: _description_
    """
    return random_post_generator(int(ENV_PERF_SIZE))


def test_perf_add_post_and_delete_several_multi_users(
    yodelr: Yodelr, several_user_names: list[str], random_post_generator_words: str
):
    logging.warning(
        "Number of post '%s' from '%s' words, and number of users '%s'",
        math.ceil(len(random_post_generator_words) / yodelr.MAX_POST_CHARS),
        ENV_PERF_SIZE,
        len(several_user_names),
    )
    for u in several_user_names:
        yodelr.add_user(u)
    m = 0
    elapsed = time()
    while yodelr.MAX_POST_CHARS * m < len(random_post_generator_words):
        user = several_user_names[random.randint(0, len(several_user_names) - 1)]
        yodelr.add_post(
            user,
            random_post_generator_words[
                yodelr.MAX_POST_CHARS * m : (m + 1) * yodelr.MAX_POST_CHARS
            ],
            m,
        )
        m += 1
    logging.warning("Time in seconds 'add_post': %s", time() - elapsed)
    elapsed = time()
    for u in several_user_names:
        yodelr.delete_user(u)
    logging.warning("Time in seconds 'delete_user': %s", time() - elapsed)


def test_perf_add_post_and_all_getters_with_multi_users(
    yodelr: Yodelr, user_names: list[str], random_post_generator_words: str
):
    logging.warning(
        "Number of post '%s' from '%s' words",
        math.ceil(len(random_post_generator_words) / yodelr.MAX_POST_CHARS),
        ENV_PERF_SIZE,
    )
    for u in user_names:
        yodelr.add_user(u)
    m = 0
    elapsed = time()
    while yodelr.MAX_POST_CHARS * m < len(random_post_generator_words):
        user = user_names[random.randint(0, len(user_names) - 1)]
        yodelr.add_post(
            user,
            random_post_generator_words[
                yodelr.MAX_POST_CHARS * m : (m + 1) * yodelr.MAX_POST_CHARS
            ],
            m,
        )
        m += 1
    logging.warning("Time in seconds 'add_post': %s", time() - elapsed)
    elapsed = time()
    for user in user_names:
        yodelr.get_posts_for_user(user)
    logging.warning("Time in seconds 'get_posts_for_user': %s", time() - elapsed)
    elapsed = time()
    for topic in yodelr._test_get_all_topics():
        yodelr.get_posts_for_topic(topic)
    logging.warning("Time in seconds 'get_posts_for_topic': %s", time() - elapsed)
    elapsed = time()
    for topic in yodelr._test_get_all_topics():
        yodelr.get_trending_topics(0, len(random_post_generator_words) - 1)
    logging.warning("Time in seconds 'get_trending_topics': %s", time() - elapsed)
