import json
import yodelr
import logging
import re
from typing import Any, List
from datastruct import StackWrapper

type Timestamp = int
type Topic = str
type Post = str
type User = str
type Stack = list

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class YodelrV1(yodelr.Yodelr):

    ID_POST: str = "post_text"
    ID_TOPICS: str = "topics"
    ID_USER: str = "author"
    REGEX_TOPIC = r"#([0-9a-zA-Z_]+)"

    def __init__(self):
        """Initialise 3 indexes to modelise YodelrV1

        Format:
        -------

        $timestamp:
            $ID_USER:       $user
            $ID_POST:       $post
            $ID_TOPICS:     Dict[$topic, int]      # key=$topic, value=occurence

        In addition, we keep track of a monotonically history
        """
        super().__init__()

        self.__data_by_timestamp: dict[Timestamp, dict[str, Any]] = dict()
        self.__timestamps_by_user: dict[User, Stack[Timestamp]] = dict()

    def add_user(self, user_name: str) -> None:
        """Add user to the system.

        Insert user_name within index:posts_by_user

        Args:
            user_name (str): user_name
        """
        logger.info("Adding user %s ...", user_name)
        self.__timestamps_by_user.setdefault(user_name, [])
        logger.debug("updated Yodelr: %s", self)

    def add_post(self, user_name: str, post_text: str, timestamp: int) -> None:
        """Add post to system

        Algorithm:
        1.  Get topics from post_text
        2.  Add user to Index(user,timestamp)
        3a.  Save topic in DATA index
        3b.  Save post in DATA index
        3c.  Save user in DATA index

        Args:
            user_name (str): _description_
            post_text (str): _description_
            timestamp (int): _description_
        """
        logger.info("Add post...")
        logger.debug(
            "associate timestamp '%s' of the post to user '%s'", timestamp, user_name
        )
        topics = self._extract_topics(post_text)
        # Update index Timestamp->{$post, $topics, $user}
        self.__data_by_timestamp[timestamp] = {
            self.ID_POST: post_text,
            self.ID_TOPICS: topics,
            self.ID_USER: user_name,
        }
        # Update reverse index User->Timestamps
        user_timestamps = self.__timestamps_by_user.setdefault(user_name, [])
        StackWrapper.add(user_timestamps, timestamp)
        logger.debug("updated Yodelr: %s", self)

    def delete_user(self, user_name: str) -> None:
        """Delete user and all its posts

        Algorithm:
        1. Fetch timestamps from user in Index(user,timestamp)
        2. Delete the user reference from Index(user,timestamp)
        3. For each $timestamp in $timestamps
        4.      Delete $timestamp from Index(timestamp,DATA)

        Complexity:
            Time:   O(T) with T size of $timestamps

        Args:
            user_name (str): user
        """
        logger.info("Deleting user '%s'...", user_name)
        timestamps = self.__timestamps_by_user.get(user_name, None)
        logger.debug("Timestamps from user '%s': %s", user_name, timestamps)
        if timestamps is None:
            # Raise exception UserNotRegistedError
            return
        logger.debug("Delete user '%s' from Index(user,timestamps)", user_name)
        del self.__timestamps_by_user[user_name]
        for timestamp in timestamps:
            del self.__data_by_timestamp[timestamp]

    def get_posts_for_user(self, user_name: str) -> List[str]:
        pass

    def get_posts_for_topic(self, topic: str) -> List[str]:
        pass

    def get_trending_topics(self, from_timestamp: int, to_timestamp: int) -> List[str]:
        pass

    def _is_user_in_system(self, user: User) -> bool:
        """[For test only]

        Args:
            user (User): _description_

        Returns:
            bool: _description_
        """
        logger.debug("Yodelr: %s", self)
        return user in self.__timestamps_by_user

    def _is_post_in_system(self, user_name: User, post_text: str) -> bool:
        """[For test only]

        Args:
            user (User): _description_

        Returns:
            bool: _description_
        """
        logger.debug("Yodelr: %s", self)
        timestamps = self.__timestamps_by_user[user_name]
        cond1 = post_text in [
            self.__data_by_timestamp[ts][self.ID_POST] for ts in timestamps
        ]
        cond2 = user_name in self.__timestamps_by_user
        return cond1 and cond2

    def _post_has_topic(self, post: Post, topic: str):
        return

    @classmethod
    def _extract_topics(cls, post_text: str) -> list[Topic]:
        """Extract all term starting with '#' matching $REGEX_TOPIC

        Args:
            post_text (str): post

        Returns:
            list[Topic]: topics
        """
        topics = re.findall(cls.REGEX_TOPIC, post_text)
        logger.debug("Topics found: %s", topics)
        return topics

    def __repr__(self) -> str:
        return f"Index(user,timestamp): {json.dumps(self.__timestamps_by_user)}"
