from abc import ABC, abstractmethod
import math


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
        """Return "top_priority" as the most prioritised in the data structure"""
        pass

    @classmethod
    @abstractmethod
    def sort(cls, l: list[T], descending: bool = False) -> list[T]:
        """Sorting method"""
        pass


class LIFOWrapper[T](DataStructWrapper):
    """Index order - Add at the end of the list
    0           -> first added, last out
    len(queue)  -> latest added, first out
    """

    # My bad
    @classmethod
    def add(cls, l: list[T], e: T) -> None:
        """Stack $e at the end (top)

        Args:
            l (list[str]): stack
            e (str): element
        """
        l.append(e)

    @classmethod
    def delete(cls, l: list[T]) -> T:
        """Remove the top priority (LIFO)

        Args:
            l (list[T]): Stack of element

        Returns:
            T: element
        """
        return l.pop(-1)

    @classmethod
    def first_out(cls, l: list[T]) -> T:
        """LIFO - Return the latest element added (top_priority) on the stack without removing it

        Args:
            l (list[T]): Stack of element

        Returns:
            T: element
        """
        if len(l) == 0:
            raise IndexError("ERR: empty list.")
        return l[-1]

    @classmethod
    def sort(cls, l: list[T], descending: bool = False) -> list[T]:
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
            l (list[str]): queue
            e (str): element
        """
        # NOTE concatenation o(k+n) ≈ O(n) -- create new list out of two list.. not good
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
            l (list[T]): Stack of element

        Returns:
            T: element
        """
        return l.pop(-1)

    @classmethod
    def first_out(cls, l: list[T]) -> T:
        """FIFO - Return the first arrived (top_priority) in queue without removing it

        Args:
            l (list[T]): queue of element

        Returns:
            T: element
        """
        if len(l) == 0:
            raise IndexError("ERR: empty list.")
        return l[-1]

    @classmethod
    def sort(cls, l: list[T], descending: bool = False) -> list[T]:
        """Sorting method"""
        pass


type IntStr = tuple[int, str]


class MaxHeapBinome[IntStr](FIFOWrapper):
    """Index order
    0           -> newest added, top priority
    len(queue)  -> less priority

    Interpret the list as heap:
    Reading from 0 to len(list) ->  Breadth-First Traversal (from root, level by level)
    """

    IND_COUNT = 0
    IND_TOPIC = 1

    @classmethod
    def has_priority_over(cls, t1: tuple[IntStr], t2: tuple[IntStr]) -> bool:
        """Compare t1 with t2 and return whether t1 has over priority over t2

        Args:
            t1 (tuple[IntStr]): to compare
            t2 (tuple[IntStr]): compared with

        Returns:
            bool: True if t1 more priority than t2 else False
        """
        return t1[cls.IND_COUNT] > t2[cls.IND_COUNT] or (
            t1[cls.IND_COUNT] == t2[cls.IND_COUNT]
            # current topic comes before parent topic ALPHABETICALLY
            and t1[cls.IND_TOPIC] < t2[cls.IND_TOPIC]
        )

    @classmethod
    def add(cls, l: list[IntStr], e: tuple) -> None:
        """Add $e to the heap respecting the following:

        1. Heap structure must be complete tree (at all time)
        2. Root node must be the highest value
        3. Left child node is calculated such as -> 2*i+1 with i from 0 to len(l)-1
        4. Right child node is calculated such as -> 2*(i+1) with i from 0 to len(l)-1
        5. Parent node is calculated such as -> int(i/2)

        Args:
            l (list[str]): queue
            e (str): element
        """
        # NOTE concatenation create new list out of two list -> o(k+n) ≈ O(n)
        # Add element to the end, respect complete tree
        l.append(e)
        get_parent = lambda ind: int(ind / 2)
        # adjust heap to max heap
        current = len(l) - 1
        # while am i not at the root
        while current != 0:
            parent = get_parent(current)
            if cls.has_priority_over(l[current], l[parent]):
                l[current], l[parent] = l[parent], l[current]
            current = parent
        print("updated heap=", l)

    @classmethod
    def delete(cls, l: list[IntStr]) -> tuple:
        """Remove the top priority (FIFO)

        1. Heap structure must be complete tree (at all time)
        2. Root node must be the highest value
        3. Left child node is calculated such as -> 2*i+1 with i from 0 to len(l)-1
        4. Right child node is calculated such as -> 2*(i+1) with i from 0 to len(l)-1
        5. Parent node is calculated such as -> int(i/2)

        Args:
            l (list[IntStr]): Stack of element

        Returns:
            tuple: element
        """
        # Last element become root then root is deleted
        l[0], l[-1] = l[-1], l[0]
        # Delete the root
        e = l.pop()
        # we compare the root down to the leaf
        get_left = lambda i: 2 * i + 1
        get_right = lambda i: 2 * (i + 1)
        # get_parent = lambda i: int(i / 2)
        current = 0  # start
        # while there is a leaf available to be compared with
        while current < len(l):
            left = get_left(current)
            right = get_right(current)
            print(f"> heap={l}")
            print(f"> current={current} left={left} right={right}")
            # parent = get_parent(current)
            if left < len(l) and right < len(l):
                print("> left and right leaves")
                # take the top priority between sibling to get the direction to leaf
                top_priority = (
                    left if cls.has_priority_over(l[left], l[right]) else right
                )
                # compare the current node with top_priority
                print(
                    f"> top priority is {'LEFT' if top_priority == left else 'RIGHT'}"
                )
                if cls.has_priority_over(l[top_priority], l[current]):
                    print(">> swap")
                    l[top_priority], l[current] = l[current], l[top_priority]
                current = top_priority

            # if there is not right, it can have a left BUT if there is not left it MUST NOT have a right
            elif left < len(l):
                print("> only left leaf")
                # compare with its parent
                if cls.has_priority_over(l[left], l[current]):
                    print(">> swap")
                    l[current], l[left] = l[left], l[current]
                current = left
            else:
                break
        print(f"{e} is deleted updated heap=", l)
        return e

    @classmethod
    def first_out(cls, l: list[IntStr]) -> tuple:
        """FIFO - Return the most priority (far left) in queue without removing it

        Args:
            l (list[IntStr]): queue of element

        Returns:
            tuple: element
        """
        if len(l) == 0:
            raise IndexError("ERR: no top priority in empty Queue.")
        return l[0]

    @classmethod
    def sort(cls, l: list[IntStr], descending: bool = False) -> list[IntStr]:
        """Heapsort

        Args:
            l (list[IntStr]): _description_
            descending (bool, optional): _description_. Defaults to False.

        Returns:
            list[IntStr]: _description_
        """
        print("START SORT", l)
        length = len(l)
        if len(l) > 0:
            e = cls.delete(l)
            print(f"$ before recur. e={e} is deleted from {l}")
            cls.sort(l)
            FIFOWrapper.add(l, e)
            print(f"$ after recur. e={e} is deleted from {l}")
        print("END SORT")
        return l


if __name__ == "__main__":
    maxheap = [
        (33, "t"),
        (28, "t"),
        (25, "t"),
        (8, "t"),
        (15, "t"),
        (21, "t"),
        (1, "t"),
    ]
    MaxHeapBinome.sort(maxheap)
    print("FINAL SORTED HEAP", maxheap)
