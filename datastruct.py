from abc import ABC
from typing import List


class DataStructWrapper[T](ABC):

    pass


class StackWrapper[T](DataStructWrapper):
    """Index order
    0           -> first added (biggest timestamp)
    len(queue)  -> newest added (smallest timestamp)
    """

    # My bad
    @staticmethod
    def add(stack: List[T], e: T) -> None:
        """Add element $e at the top of the $stack

        Args:
            stack (List[str]): stack
            e (str): element
        """
        stack.append(e)

    @staticmethod
    def pop(stack: List[T]) -> T:
        """Remove the top of the stack and return it

        Args:
            stack (List[T]): Stack of element

        Returns:
            T: element
        """
        return stack.pop()

    @staticmethod
    def top(stack: List[T]) -> T:
        """Return the top of the stack without removing it.

        Args:
            stack (List[T]): Stack of element

        Returns:
            T: element
        """
        return stack[-1]


class QueueWrapper[T](DataStructWrapper):
    """Index order
    0           -> newest added (biggest timestamp)
    len(queue)  -> first added (smallest timestamp)
    """

    @staticmethod
    def add(queue: List[T], e: T) -> None:
        """Add element $e in the queue

        Args:
            queue (List[str]): queue
            e (str): element
        """
        # NOTE concatenation o(k+n) ≈ O(n)
        # NOTE concatenation create new list out of two list.. not good
        if len(queue) > 0:
            queue.append(queue[-1])
            i = len(queue) - 2
            while i > 0:
                queue[i] = queue[i - 1]
                i -= 1
            queue[0] = e
        else:
            queue.append(e)

    @staticmethod
    def first(queue: List[T]) -> T:
        """Return the first in queue without removing it

        Args:
            queue (List[T]): queue of element

        Returns:
            T: element
        """
        return queue[-1]
