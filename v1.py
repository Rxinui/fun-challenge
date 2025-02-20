import yodelr


type Timestamp = int
type Topic = str
type User = str
type Stack = list


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

    
