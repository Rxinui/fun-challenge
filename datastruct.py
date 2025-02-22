from abc import ABC, abstractmethod, abstractstaticmethod
from typing import List


class DataStructWrapper[T](ABC):

    @staticmethod
    @abstractmethod
    def add(l: List[T], e: T) -> None:
        pass

    @staticmethod
    @abstractmethod
    def delete(l: List[T]) -> T:
        pass

    @staticmethod
    @abstractmethod
    def top_priority(l: List[T]) -> T:
        """Return "top_priority" as the most prioritised in the data structure"""
        pass


class StackWrapper[T](DataStructWrapper):
    """Index order
    0           -> top priority (biggest timestamp)
    len(queue)  -> newest added (smallest timestamp)
    """

    # My bad
    @staticmethod
    def add(l: List[T], e: T) -> None:
        """Add element $e at the top of the stack

        Args:
            l (List[str]): stack
            e (str): element
        """
        l.append(e)

    @staticmethod
    def delete(l: List[T]) -> T:
        """Remove the top of the stack and return it

        Args:
            l (List[T]): Stack of element

        Returns:
            T: element
        """
        return l.pop()

    @staticmethod
    def top_priority(l: List[T]) -> T:
        """Return the latest element added (top_priority) on the stack without removing it

        Args:
            l (List[T]): Stack of element

        Returns:
            T: element
        """
        if len(l) == 0:
            raise IndexError("ERR: no top priority in empty Stack.")
        return l[0]


class QueueWrapper[T](DataStructWrapper):
    """Index order
    0           -> newest added (biggest timestamp)
    len(queue)  -> top priority (smallest timestamp)
    """

    @staticmethod
    def add(l: List[T], e: T) -> None:
        """Add element $e in the queue

        Args:
            l (List[str]): queue
            e (str): element
        """
        # NOTE concatenation o(k+n) ≈ O(n)
        # NOTE concatenation create new list out of two list.. not good
        if len(l) > 0:
            l.append(l[-1])
            i = len(l) - 2
            while i > 0:
                l[i] = l[i - 1]
                i -= 1
            l[0] = e
        else:
            l.append(e)

    @staticmethod
    def delete(l: List[T]) -> T:
        """Remove the top of the stack and return it

        Args:
            l (List[T]): Stack of element

        Returns:
            T: element
        """
        return None

    @staticmethod
    def top_priority(l: List[T]) -> T:
        """Return the first arrived (top_priority) in queue without removing it

        Args:
            l (List[T]): queue of element

        Returns:
            T: element
        """
        if len(l) == 0:
            raise IndexError("ERR: no top priority in empty Queue.")
        return l[-1]
