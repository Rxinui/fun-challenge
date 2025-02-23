# Copyright Vespa.ai.
# Not for redistribution outside of candidate interview context.

from abc import ABC, abstractmethod
from typing import List


class Yodelr(ABC):
    """
    The Yodelr service interface.

    This allows adding and deleting users, adding and retrieving posts
    and getting trending topics.
    """

    @abstractmethod
    def add_user(self, user_name: str) -> None:
        pass

    @abstractmethod
    def add_post(self, user_name: str, post_text: str, timestamp: int) -> None:
        pass

    @abstractmethod
    def delete_user(self, user_name: str) -> None:
        pass

    @abstractmethod
    def get_posts_for_user(self, user_name: str) -> List[str]:
        pass

    @abstractmethod
    def get_posts_for_topic(self, topic: str) -> List[str]:
        pass

    @abstractmethod
    def get_trending_topics(self, from_timestamp: int, to_timestamp: int) -> List[str]:
        pass


class YodelrError(Exception):

    UNKNOWN_USER = 100

    def __init__(self, error_code: int, message: str = ""):
        self.error_code = error_code
        super().__init__(f"(ERR={self.error_code}) {message}".strip())
