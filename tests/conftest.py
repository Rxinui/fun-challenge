import pytest

@pytest.fixture(scope="module")
def user_name() -> str:
    return "Rxinui"


@pytest.fixture(scope="module")
def sample_10_posts() -> list[str]:
    return [
        "My very #first #test post.",
        "Post with odd index has no topic",
        "Random #post for test",
        "same here, no topic!",
        "#post is posted",
        "still no topic in the post",
        "new #post inserted",
        "told you, none, nada!",
        "totally #unique #tweet",
    ]


@pytest.fixture(scope="module")
def current_timestamp() -> int:
    """Emulate timestamp by a simple counter

    The usage of time.time() to represent timestamp in
    3 instructions in a row, result to the same value if
    cast to integer (Yodelr API spec), hence false value.

    Returns:
        int: timestamp
    """
    mock_epoch += 1
    return mock_epoch
