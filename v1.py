import logging
import re
from typing import Any, List
from yodelr import Yodelr, YodelrError
from internal.datastruct import MinHeapBinome
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

    def __init__(self, fast_write: bool = True):
        """Initialise 3 indexes to modelise YodelrV1

        About Wrapper:
        - LIFO: if chosen as WrapperOnAdd, it optimises performance on addPost (fast_write) and impacts getPost
        - FIFO: if chosen as WrapperOnAdd, it optimises performance on getPost* and impacts addPost
        - if LIFO is chosen as WrapperOnAdd then FIFO is taken by WrapperOnGet (vice versa)

        About timestamps_by_topic:
        - For a given $topic, its list of timestamps can have duplicates because if one post contains 2 $topic that are equals, the timestamp is added 2 times (and so forth)
        - Having duplicates is handy for getTrendingTopics to calculate the count (sum of a bitmap)

        Format:
        -------
        data_by_timestamp:
            $timestamp:
                $ID_USER:       $user
                $ID_POST:       $post
                $ID_TOPICS:     Dict[$topic, int]      # key=$topic, value=occurence
        """
        super().__init__()
        self._posts: list[Post] = []
        self._inverted_composite_index: dict[
            Topic | Timestamp | User, List[int] | int
        ] = dict()

    def add_user(self, user_name: str) -> None:
        """Add user to the system.

        Insert user_name within Dict(user,timestamp)

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
        1.  Get topics from post_text
        2.  Add user to Dict(user,timestamp)
        3a.  Save topic in DATA index
        3b.  Save post in DATA index
        3c.  Save user in DATA index

        Args:
            user_name (str): _description_
            post_text (str): _description_
            timestamp (int): _description_
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
            if ind not in self._inverted_composite_index.get(topic, []):
                self._inverted_composite_index.setdefault(topic, []).append(ind)
        logger.debug("> updated Yodelr: %s", self)

    def delete_user(self, user_name: str) -> None:
        """Delete user and all its posts

        Algorithm:
        1. Fetch timestamps from user in Dict(user,timestamp)
        2. Delete the user reference from Dict(user,timestamp)
        3. For each $timestamp in $timestamps
        4.      Delete $timestamp from Dict(timestamp,DATA)

        Complexity:
            Time:   O(T) with T size of $timestamps

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
            self._posts[ind] = None  # mark as removed

    def get_posts_for_user(self, user_name: str) -> List[str]:
        """Get list of post from a user

        Args:
            user_name (str): user

        Algorithm:
            Initialise an empty $WrapperOnGet for posts
            Fetch timestamps in Dict(user,timestamps)
            For-each $timestamp in $timestamps
                Get $post using $timestamp in Dict(timestamp,DATA)
                Add $post on top of the $WrapperOnGet $posts
            Return the $WrapperOnGet $posts

        Returns:
            List[str]: posts (as $WrapperOnGet)
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
            Initialise an empty $WrapperOnGet for posts
            Fetch timestamps in Dict(topic,timestamps)
            For-each $timestamp in $timestamps
                Get $post using $timestamp in Dict(timestamp,DATA)
                Add $post on top of the $WrapperOnGet $posts
            Return the $WrapperOnGet $posts


        Args:
            topic (str): _description_

        Returns:
            List[str]: _description_
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
            Init a new list for topics -> trends
            For each timestamp between $to_timestamp and $from_timestamp
                Retrieve $topics in Dict($timestamp,DATA)
                Retrieve count of $topic by applying 'len' to timestamps of Dict($topic,timestamps)
                Create a tuple containing ($topic, $count) -> trend
                If $trends is empty then
                    Add a $trend to $trends
                If $trend.count > first_out($trends)
                    Enqueue $trend to $trends
                Else
                    Stack up $trend to $trends
            Return $trends

        Args:
            from_timestamp (int): start trends period
            to_timestamp (int): end trends period

        Returns:
            List[str]: _description_
        """
        if from_timestamp > to_timestamp:
            from_timestamp, to_timestamp = to_timestamp, from_timestamp
        logger.info(
            "Get trending topics from=%s to=%s...", from_timestamp, to_timestamp
        )
        trends = []
        topics = dict()
        logger.debug("> 1st pass topics=%s", topics)
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
            topic = match.group(0)  # we keep hashtag
            if topic not in topics:
                topics.append(topic)
        logger.debug("Topics found: %s", topics)
        return topics

    def __repr__(self) -> str:
        return f"""Inverted Composite Index: {self._inverted_composite_index}
Total posts: {len(self._posts)}
"""
