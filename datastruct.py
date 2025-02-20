from typing import List


class StackWrapper[T: (str, int)]:

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
