from abc import ABC, abstractmethod


class DataStructWrapper[T](ABC):

    @classmethod
    @abstractmethod
    def add(cls, l: list[T], e: T) -> None:
        pass

    @classmethod
    @abstractmethod
    def delete(cls, l: list[T]) -> T:
        pass

    @classmethod
    @abstractmethod
    def first_out(cls, l: list[T]) -> T:
        pass

    @classmethod
    @abstractmethod
    def sort(cls, l: list[T]) -> list[T]:
        pass


class LIFOWrapper[T](DataStructWrapper):
    """Index order - Add at the end of the list
    0           -> first added, last out
    len(queue)  -> latest added, first out
    """

    @classmethod
    def add(cls, l: list[T], e: T) -> None:
        """Stack $e at the end (top)

        Args:
            l (list[str]): list
            e (str): element
        """
        l.append(e)

    @classmethod
    def delete(cls, l: list[T]) -> T:
        """Remove the top priority (LIFO)

        Args:
            l (list[T]): list

        Returns:
            T: element
        """
        return l.pop(-1)

    @classmethod
    def first_out(cls, l: list[T]) -> T:
        """LIFO - Return the latest element added (top_priority) on the stack without removing it

        Args:
            l (list[T]): list

        Returns:
            T: element
        """
        if len(l) == 0:
            raise IndexError("ERR: empty list.")
        return l[-1]

    @classmethod
    def sort(cls, l: list[T]) -> list[T]:
        """Sorting method"""
        pass


class FIFOWrapper[T](DataStructWrapper):
    """Index order - Add from the beginning (enqueue)
    0           -> last added, last out
    len(queue)  -> first added, first out
    """

    @classmethod
    def add(cls, l: list[T], e: T) -> None:
        """Enqueue $e at the beginning

        Args:
            l (list[str]): list
            e (str): element
        """
        # NOTE concatenation o(k+n) ≈ O(n) -- create new list out of two list.. not good
        # we do it in-place using sliding window
        if len(l) > 0:
            l.append(l[-1])
            i = len(l) - 2
            while i > 0:
                l[i] = l[i - 1]
                i -= 1
            l[0] = e
        else:
            l.append(e)

    @classmethod
    def delete(cls, l: list[T]) -> T:
        """Remove the top priority (FIFO)

        Args:
            l (list[T]): list

        Returns:
            T: element
        """
        return l.pop(-1)

    @classmethod
    def first_out(cls, l: list[T]) -> T:
        """FIFO - Return the first arrived (top_priority) in queue without removing it

        Args:
            l (list[T]): list

        Returns:
            T: element
        """
        if len(l) == 0:
            raise IndexError("ERR: empty list.")
        return l[-1]

    @classmethod
    def sort(cls, l: list[T]) -> list[T]:
        """Sorting method"""
        pass
