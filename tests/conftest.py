import pytest
from v1 import YodelrV1 as yodelr


@pytest.fixture(scope="module")
def user_name() -> str:
    return "Rxinui"


@pytest.fixture(scope="module")
def sample_10_posts() -> list[str]:
    return [
        "My very #first #test post.",
        "Post with odd index has no topic",
        "Random #post for #test",
        "same here, no topic!",
        "#post is posted",
        "still no topic in the post",
        "new #post inserted",
        "told you, none, nada!",
        "totally #unique #tweet",
    ]


@pytest.fixture(scope="module")
def sample_10_posts_and_topics(sample_10_posts: list[str]) -> list[tuple[str, list]]:
    return [(post, yodelr._extract_topics(post)) for post in sample_10_posts]
