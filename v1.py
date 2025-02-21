import yodelr
import logging
import os
from typing import List
from datastruct import StackWrapper

type Timestamp = int
type Topic = str
type User = str
type Stack = list

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="[%(asctime)s] %(message)s", level=os.getenv("LOG_LEVEL") or logging.DEBUG
)


class Post:

    def __init__(self, user: User, message: str, timestamp: Timestamp):
        self.__user = user
        self.__msg = message
        self.__timestamp = timestamp

    @property
    def timestamp(self) -> Timestamp:
        """Time of post (primary key)

        Returns:
            Timestamp: time of post
        """
        return self.__timestamp

    @property
    def user(self) -> User:
        """Name of author of the post

        Returns:
            User: user name
        """
        return self.__user

    @property
    def message(self) -> str:
        """Message of the post

        Returns:
            str: message
        """
        return self.__msg


class YodelrV1(yodelr.Yodelr):

    def __init__(self):
        """Initialise 3 indexes to modelise YodelrV1
        - Posts by topic
        - Posts by user
        - Topics by timestamp

        In addition, we keep track of a monotonically history
        """
        super().__init__()
        self.__posts_by_topic: dict[Topic, Stack[Post]] = dict()
        self.__posts_by_user: dict[User, Stack[Post]] = dict()
        self.__topics_by_timestamp: dict[Topic, Stack[Timestamp]] = dict()
        self.__history: list[Timestamp] = list()

    def _is_user_in_system(self, user: User) -> bool:
        """[For test only]

        Args:
            user (User): _description_

        Returns:
            bool: _description_
        """
        return user in self.__posts_by_user

    def _is_post_in_system(self, user: User, post_text: str) -> bool:
        """[For test only]

        Args:
            user (User): _description_

        Returns:
            bool: _description_
        """
        return post_text in [p.message for p in self.__posts_by_user[user]]

    def add_user(self, user_name: str) -> None:
        """Add user to the system.

        Insert username within index:posts_by_user

        Args:
            user_name (str): username
        """
        logger.debug("Adding user %s ...", user_name)
        self.__posts_by_user[user_name] = []

    def add_post(self, user_name: str, post_text: str, timestamp: int) -> None:
        """Add post to system


        Args:
            user_name (str): _description_
            post_text (str): _description_
            timestamp (int): _description_
        """
        pass

    def delete_user(self, user_name: str) -> None:
        pass

    def get_posts_for_user(self, user_name: str) -> List[str]:
        pass

    def get_posts_for_topic(self, topic: str) -> List[str]:
        pass

    def get_trending_topics(self, from_timestamp: int, to_timestamp: int) -> List[str]:
        pass
