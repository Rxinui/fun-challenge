import logging
import re
from typing import Any, List
from yodelr import Yodelr, YodelrError
from internal.wrapper import FIFOWrapper, LIFOWrapper

type Timestamp = int
type Topic = str
type Post = str
type User = str

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class YodelrV1(Yodelr):

    ID_POST: str = "post_text"
    ID_TOPICS: str = "topics"
    ID_USER: str = "author"
    REGEX_TOPIC = r"#([0-9a-zA-Z_]+)"
    MAX_POST_CHARS = 140

    def __init__(self):
        """Initialise a composite inverted index and list of posts

        Keep track of post deleted for future improvement using
        clean-on-threshold algorithn #v3

        Composite inverted index:
            Topic:      List[int]
            User:       List[int]
            Timestamp:  int
        """
        super().__init__()
        self._posts: list[Post] = []
        self._inverted_composite_index: dict[
            Topic | Timestamp | User, List[int] | int
        ] = dict()
        self._post_deleted = 0

    def add_user(self, user_name: str) -> None:
        """Add user to the system.

        Args:
            user_name (str): user_name
        """
        logger.info("Adding user %s ...", user_name)
        self._inverted_composite_index[user_name] = []
        logger.debug("updated Yodelr: %s", self)

    def add_post(self, user_name: str, post_text: str, timestamp: int) -> None:
        """Add post to system

        If post has more than $MAX_POST_CHARS characters,
        the post will be truncated to $MAX_POST_CHARS chars.

        A topic found in post is case sensitive, therefore
        topic '#hello' is different than '#Hello'

        Algorithm:
        1. Extract topics from post
        2. Add post to posts
        3. Add indice of post in its list in inverted index timestamp
        3. Add indice of post in its list in inverted index user
        3. Add indice of post in its list in inverted index topic

        Args:
            user_name (str): user
            post_text (str): post
            timestamp (int): timestamp
        """
        logger.info("Add post...")
        if not self._is_user_in_system(user_name):
            raise YodelrError(YodelrError.UNKNOWN_USER)
        ind = len(self._posts)
        post_text = post_text[: self.MAX_POST_CHARS]
        topics = self._extract_topics(post_text)
        self._posts.append(post_text)
        self._inverted_composite_index[str(timestamp)] = ind
        self._inverted_composite_index[user_name].append(ind)
        for topic in topics:
            # NOTE no duplicate for topic
            if ind not in self._inverted_composite_index.get(topic, []):
                self._inverted_composite_index.setdefault(topic, []).append(ind)
        logger.debug("> updated Yodelr: %s", self)

    def delete_user(self, user_name: str) -> None:
        """Delete user and all its posts

        Algorithm:
        1. Get indices from inverted index user
        2. Delete user from inverted index
        3. For each indice, replace post with None to mark as deleted

        Args:
            user_name (str): user
        """
        logger.info("Deleting user '%s'...", user_name)
        user_inds = self._inverted_composite_index.get(user_name, None)
        if user_inds is None:
            raise YodelrError(YodelrError.UNKNOWN_USER)
        logger.debug("> indices of user '%s': %s", user_name, user_inds)
        logger.debug("> delete user '%s' from inverted composite index", user_name)
        del self._inverted_composite_index[user_name]
        for ind in user_inds:
            # NOTE mark as removed - policy to speed up
            self._posts[ind] = None
            self._post_deleted += 1
        # NOTE shift all post to left to downsize posts and free space
        # TODO v3 - implement clean-on-threshold to free space on self._posts

    def get_posts_for_user(self, user_name: str) -> List[str]:
        """Get list of post from a user

        Args:
            user_name (str): user

        Algorithm:
        1. Get indices from inverted index user
        2. For each indices, enqueue post to posts
        3. Return posts

        Returns:
            List[str]: posts
        """
        logger.info("Get posts for user '%s'...", user_name)
        posts: list = []
        user_inds = self._inverted_composite_index.get(user_name, None)
        if user_inds is None:
            raise YodelrError(YodelrError.UNKNOWN_USER)
        logger.debug("> indices of user '%s': %s", user_name, user_inds)
        for ind in user_inds:
            FIFOWrapper.add(posts, self._posts[ind])  # latest at ind=0
        logger.debug("> updated Yodelr: %s", self)
        return posts

    def get_posts_for_topic(self, topic: str) -> List[str]:
        """Get all posts of a topic

        Algorithm:
        1. Get indices from inverted index topic
        2. For each indices, enqueue post to posts
        3. Return posts


        Args:
            topic (str): topic

        Returns:
            List[str]: posts
        """
        logging.info("Get posts for topic...")
        posts = []
        topic_inds = self._inverted_composite_index.get(f"#{topic}", [])
        logger.debug("> indices of topic '%s': %s", topic, topic_inds)
        for ind in topic_inds:
            FIFOWrapper.add(posts, self._posts[ind])
        return posts

    def get_trending_topics(self, from_timestamp: int, to_timestamp: int) -> List[str]:
        """Get topics trending in a specific timespan

        Algorithm:
        1. For each timestamp between from and to
        2. Get indice from inverted index timestamp
        3. If there is a post then
            4.  Extract topics from post
            5.  Count total topic in all post for each topic
            6.  Create trends by using topic and its count
            7.  Sort trends primarily by DESC count then ASC alphabetically
        8. Return trends

        Args:
            from_timestamp (int): start trends period
            to_timestamp (int): end trends period

        Returns:
            List[str]: topics
        """
        # NOTE no exception, permutation to fix
        if from_timestamp > to_timestamp:
            from_timestamp, to_timestamp = to_timestamp, from_timestamp
        logger.info(
            "Get trending topics from=%s to=%s...", from_timestamp, to_timestamp
        )
        trends = []
        topics = dict()
        logger.debug("> 1st pass topics=%s", topics)
        # TODO v3 - implement binary search for closest timestamp
        for ts in range(from_timestamp, to_timestamp + 1):
            ind = self._inverted_composite_index.get(str(ts), None)
            if ind is not None and self._posts[ind] is not None:
                tps = self._extract_topics(self._posts[ind])
                for topic in tps:
                    topic = topic.lstrip("#")
                    if topic not in topics:
                        topics[topic] = 1
                    else:
                        topics[topic] += 1
        logger.debug("> 2nd pass topics with count=%s", topics)
        trends = []
        for topic, count in topics.items():
            trends.append((count, topic))
            logger.debug(">> trends=%s", trends)
        # NOTE sorting: desc on count, alpha asc on topic
        trends.sort(key=lambda tup: (-tup[0], tup[1]))
        trends = [trend[1] for trend in trends]
        logger.debug("> 3rd pass trends=%s", trends)
        return trends

    def _is_user_in_system(self, user: User) -> bool:
        """Check if user registered in system

        Args:
            user (User): _description_

        Returns:
            bool: _description_
        """
        return user in self._inverted_composite_index

    def _test_is_post_in_system(self, user_name: User, post_text: str) -> bool:
        """[FOR TEST ONLY]

        Args:
            user (User): _description_

        Returns:
            bool: _description_
        """
        return (
            self._inverted_composite_index.get(user_name, False)
            and post_text in self._posts
        )

    def _test_get_all_topics(self) -> list[Topic]:
        """[FOR TEST ONLY]

        Returns:
            list[Topic]: all topic
        """
        return list(
            filter(lambda k: k.startswith("#"), self._inverted_composite_index.keys())
        )

    def _test_check_post_in_system(self, timestamp: Timestamp) -> bool:
        """[FOR TEST ONLY]

        Returns:
            list[Topic]: all topic
        """
        return self._inverted_composite_index.get(timestamp, False)

    @classmethod
    def _extract_topics(cls, post_text: str, case_sensitive=True) -> list[Topic]:
        """Extract all term starting with '#' matching $REGEX_TOPIC

        Args:
            post_text (str): post

        Returns:
            list[Topic]: topics
        """
        # NOTE re.findall takes duplicates as well which is not handy for us
        # NOTE re.findall goes through the whole string, then O(n)
        # topics = re.findall(cls.REGEX_TOPIC, post_text)
        if not case_sensitive:
            post_text = post_text.lower()
        topics = []
        for match in re.finditer(cls.REGEX_TOPIC, post_text):
            # NOTE we keep hashtag
            topic = match.group(0)
            if topic not in topics:
                topics.append(topic)
        logger.debug("Topics found: %s", topics)
        return topics

    def __repr__(self) -> str:
        return f"""Inverted Composite Index: {self._inverted_composite_index}
Total posts: {len(self._posts)}
"""
