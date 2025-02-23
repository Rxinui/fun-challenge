import json
import yodelr
import logging
import re
from typing import Any, List
from datastruct import MaxHeapOfTupleWrapper, FIFOWrapper, LIFOWrapper

type Timestamp = int
type Topic = str
type Post = str
type User = str
type Stack = list  # wrong !
type Queue = list

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class YodelrV1(yodelr.Yodelr):

    ID_POST: str = "post_text"
    ID_TOPICS: str = "topics"
    ID_USER: str = "author"
    REGEX_TOPIC = r"#([0-9a-zA-Z_]+)"

    def __init__(self):
        """Initialise 3 indexes to modelise YodelrV1

        About Wrapper:
        - Stack: if chosen as WrapperOnAdd, it optimises performance on addPost and impacts getPost
        - Queue: if chosen as WrapperOnAdd, it optimises performance on getPost* and impacts addPost
        - if Stack is chosen as WrapperOnAdd then Queue is taken by WrapperOnGet (vice versa)

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

        In addition, we keep track of a monotonically history
        """
        super().__init__()
        self.__WrapperOnAdd = LIFOWrapper
        self.__WrapperOnGet = FIFOWrapper
        self.__data_by_timestamp: dict[Timestamp, dict[str, Any]] = dict()
        self.__timestamps_by_user: dict[User, list[Timestamp]] = dict()
        # Because of the way I represent timestamps by topic
        # WrapperOnAdd should be LIFOWrapper as addPost is costly because
        # of the indexation of Topic
        self.__timestamps_by_topic: dict[Topic, list[Timestamp]] = dict()

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
            "> associate timestamp '%s' of the post to user '%s'", timestamp, user_name
        )
        topics = self._extract_topics(post_text)
        # Indexation of Timestamp->{$post, $topics, $user}
        self.__data_by_timestamp[timestamp] = {
            self.ID_POST: post_text,
            self.ID_TOPICS: topics,
            self.ID_USER: user_name,
        }
        # Indexation of Topic->Timestamps
        for topic in topics:
            topic_timestamps = self.__timestamps_by_topic.setdefault(topic, [])
            # Keep duplicate timestamp away
            if (
                len(topic_timestamps) > 0
                and self.__WrapperOnAdd.first_out(topic_timestamps) != timestamp
            ) or len(topic_timestamps) == 0:
                self.__WrapperOnAdd.add(topic_timestamps, timestamp)

        # Indexation of User->Timestamps
        user_timestamps = self.__timestamps_by_user.setdefault(user_name, [])
        self.__WrapperOnAdd.add(user_timestamps, timestamp)
        logger.debug("> updated Yodelr: %s", self)

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
        logger.debug("> timestamps from user '%s': %s", user_name, timestamps)
        if timestamps is None:
            # Raise exception UserNotRegisteredError
            return
        logger.debug("> delete user '%s' from Index(user,timestamps)", user_name)
        del self.__timestamps_by_user[user_name]
        for timestamp in timestamps:
            del self.__data_by_timestamp[timestamp]

    def get_posts_for_user(self, user_name: str) -> List[str]:
        """Get list of post from a user

        Args:
            user_name (str): user

        Algorithm:
            Initialise an empty $WrapperOnGet for posts
            Fetch timestamps in Index(user,timestamps)
            For-each $timestamp in $timestamps
                Get $post using $timestamp in Index(timestamp,DATA)
                Add $post on top of the $WrapperOnGet $posts
            Return the $WrapperOnGet $posts

        Returns:
            List[str]: posts (as $WrapperOnGet)
        """
        logger.info("Get posts for user '%s'...", user_name)
        posts: list = []
        timestamps = self.__timestamps_by_user.get(user_name, None)
        logger.debug("> timestamps=%s", timestamps)
        if timestamps is None:
            # raise exception UserNotRegisteredError
            return
        for timestamp in timestamps:
            post = self.__data_by_timestamp[timestamp][self.ID_POST]
            self.__WrapperOnGet.add(posts, post)
            logger.debug("> post '%s' added to posts=%s", post, posts)
        logger.debug("> updated Yodelr: %s", self)
        return posts

    def get_posts_for_topic(self, topic: str) -> List[str]:
        """Get all posts of a topic

        Algorithm:
            Initialise an empty $WrapperOnGet for posts
            Fetch timestamps in Index(topic,timestamps)
            For-each $timestamp in $timestamps
                Get $post using $timestamp in Index(timestamp,DATA)
                Add $post on top of the $WrapperOnGet $posts
            Return the $WrapperOnGet $posts


        Args:
            topic (str): _description_

        Returns:
            List[str]: _description_
        """
        logging.info("Get posts for topic...")
        posts = []
        timestamps = self.__timestamps_by_topic.get(topic, None)
        logger.debug("> timestamps of topic '%s': %s", topic, timestamps)
        if timestamps is None:
            # raise an Exception
            return posts
        for timestamp in timestamps:
            post = self.__data_by_timestamp[timestamp][self.ID_POST]
            self.__WrapperOnGet.add(posts, post)
        return posts

    def get_trending_topics(self, from_timestamp: int, to_timestamp: int) -> List[str]:
        """Get topics trending in a specific timespan

        Algorithm:
            Init a new list for topics -> trends
            For each timestamp between $to_timestamp and $from_timestamp
                Retrieve $topics in Index($timestamp,DATA)
                Retrieve count of $topic by applying 'len' to timestamps of Index($topic,timestamps)
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
        logger.info(
            "Get trending topics from=%s to=%s...", from_timestamp, to_timestamp
        )
        # Phase 1: regroup all topics within the timespan
        topics = []
        for ts in range(from_timestamp, to_timestamp + 1):
            if ts not in self.__data_by_timestamp:
                continue
            topics.extend(self.__data_by_timestamp[ts][self.ID_TOPICS])
        logger.debug("> 1st pass topics=%s", topics)
        # Phase 2: counting number of topics
        topics_counter = dict()
        for topic in topics:
            if topic not in topics_counter:
                topics_counter[topic] = 1
            else:
                topics_counter[topic] += 1
        logger.debug("> 2nd pass counter=%s", topics)
        # Phase 3: creating trend based on topic its count
        trends = []
        for topic, count in topics_counter.items():
            MaxHeapOfTupleWrapper.add(trends, (count, topic))
            logger.debug(">> trends=%s", trends)
        trends = MaxHeapOfTupleWrapper.sort(trends, descending=True)
        trends = [trend[1] for trend in trends]
        logger.debug("> 3rd pass trends=%s", trends)
        return trends

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
        # NOTE re.findall takes duplicates as well which is not handy for us
        # NOTE re.findall goes through the whole string, then O(n)
        # topics = re.findall(cls.REGEX_TOPIC, post_text)
        topics = []
        for match in re.finditer(cls.REGEX_TOPIC, post_text):
            topic = match.group(0)[1:]  # remove hashtag
            if topic not in topics:
                topics.append(topic)
        logger.debug("Topics found: %s", topics)
        return topics

    def __repr__(self) -> str:
        return f"""\r
        Index(topic,timestamp): {self.__timestamps_by_topic}
        Index(user,timestamp): {self.__timestamps_by_user}
        Index(timestamp,DATA): {self.__data_by_timestamp}
        """
