import pytest
from v1 import YodelrV1 as yodelr


@pytest.fixture(scope="module")
def user_name() -> str:
    return "Rxinui"


@pytest.fixture(scope="module")
def sample_10_posts() -> list[str]:
    """
    Topic   Occurrence in corpus    Occur. in corpus per post
    -----   --------------------    -------------------------
    first   1                       1
    test    2                       2
    post    3                       3
    topic   3                       2
    full    3                       1

    Returns:
        list[str]: posts
    """
    return [
        "My very #first #test post.",
        "Post with odd index has no topic", # 1
        "Random #post for #test",
        "same here, no topic!", #3
        "#post is posted",
        "still no topic in the post",
        "new #post of #topic inserted", 
        "told you, none, nada!",
        "#full #topic #full #topic #full",
        "do you understand nil topic",
    ]


@pytest.fixture(scope="module")
def sample_10_posts_and_topics(sample_10_posts: list[str]) -> list[tuple[str, list]]:
    return [(post, yodelr._extract_topics(post)) for post in sample_10_posts]
