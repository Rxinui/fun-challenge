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
    def top_priority(cls, l: list[T]) -> T:
        """Return "top_priority" as the most prioritised in the data structure"""
        pass

    @classmethod
    @abstractmethod
    def sort(cls, l: list[T], descending: bool = False) -> list[T]:
        """Sorting method"""
        pass


class StackWrapper[T](DataStructWrapper):
    """Index order
    0           -> top priority
    len(queue)  -> newest added
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
        pass

    @classmethod
    def top_priority(cls, l: list[T]) -> T:
        """LIFO - Return the latest element added (top_priority) on the stack without removing it

        Args:
            l (list[T]): Stack of element

        Returns:
            T: element
        """
        if len(l) == 0:
            raise IndexError("ERR: no top priority in empty Stack.")
        return l[0]

    @classmethod
    def sort(cls, l: list[T], descending: bool = False) -> list[T]:
        """Sorting method"""
        pass


class QueueWrapper[T](DataStructWrapper):
    """Index order
    0           -> newest added
    len(queue)  -> top priority
    """

    @classmethod
    def add(cls, l: list[T], e: T) -> None:
        """Enqueue $e at the beginning

        Args:
            l (list[str]): queue
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

    @classmethod
    def delete(cls, l: list[T]) -> T:
        """Remove the top priority (FIFO)

        Args:
            l (list[T]): Stack of element

        Returns:
            T: element
        """
        return None

    @classmethod
    def top_priority(cls, l: list[T]) -> T:
        """FIFO - Return the first arrived (top_priority) in queue without removing it

        Args:
            l (list[T]): queue of element

        Returns:
            T: element
        """
        if len(l) == 0:
            raise IndexError("ERR: no top priority in empty Queue.")
        return l[-1]

    @classmethod
    def sort(cls, l: list[T], descending: bool = False) -> list[T]:
        """Sorting method"""
        pass


class MaxHeapWrapper[T](QueueWrapper):
    """Index order
    0           -> newest added, top priority
    len(queue)  -> less priority

    Interpret the list as heap:
    Reading from 0 to len(list) ->  Breadth-First Traversal (from root, level by level)
    """

    @classmethod
    def add(cls, l: list[T], e: T) -> None:
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
        i = len(l) - 1
        # while am i not at the root
        while i != 0:
            parent = get_parent(i)
            if l[i] > l[parent]:
                l[i], l[parent] = l[parent], l[i]
            i = parent
        print("updated heap=", l)

    @classmethod
    def delete(cls, l: list[T]) -> T:
        """Remove the top priority (FIFO)

        1. Heap structure must be complete tree (at all time)
        2. Root node must be the highest value
        3. Left child node is calculated such as -> 2*i+1 with i from 0 to len(l)-1
        4. Right child node is calculated such as -> 2*(i+1) with i from 0 to len(l)-1
        5. Parent node is calculated such as -> int(i/2)

        Args:
            l (list[T]): Stack of element

        Returns:
            T: element
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
                top_priority = left if l[left] > l[right] else right
                # compare the current node with top_priority
                print(
                    f"> top priority is {'LEFT' if top_priority == left else 'RIGHT'}"
                )
                if l[top_priority] > l[current]:
                    print(">> swap")
                    l[top_priority], l[current] = l[current], l[top_priority]
                current = top_priority

            # if there is not right, it can have a left BUT if there is not left it MUST NOT have a right
            elif left < len(l):
                print("> only left leaf")
                # compare with its parent
                if l[left] > l[current]:
                    print(">> swap")
                    l[current], l[left] = l[left], l[current]
                current = left
            else:
                break
        print(f"{e} is deleted updated heap=", l)
        return e

    @classmethod
    def top_priority(cls, l: list[T]) -> T:
        """FIFO - Return the most priority (far left) in queue without removing it

        Args:
            l (list[T]): queue of element

        Returns:
            T: element
        """
        if len(l) == 0:
            raise IndexError("ERR: no top priority in empty Queue.")
        return l[0]

    @classmethod
    def sort(cls, l: list[T], descending: bool = False) -> list[T]:
        """Sorting method"""
        print("START SORT", l)
        length = len(l)
        nl = [None] * length
        if descending:
            k = 0
            c = 1
        else:
            k = length - 1
            c = -1
        for i in range(length):
            nl[i * c + k] = cls.delete(l)
        print("END SORT", nl)
        return nl


type TupleCountTopic = tuple[int, int]


class MaxHeapOfTupleWrapper[TupleCountTopic](QueueWrapper):
    """Index order
    0           -> newest added, top priority
    len(queue)  -> less priority

    Interpret the list as heap:
    Reading from 0 to len(list) ->  Breadth-First Traversal (from root, level by level)
    """

    IND_COUNT = 0
    IND_TOPIC = 1

    @classmethod
    def add(cls, l: list[TupleCountTopic], e: tuple) -> None:
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
            if l[current][cls.IND_COUNT] > l[parent][cls.IND_COUNT] or (
                l[current][cls.IND_COUNT] == l[parent][cls.IND_COUNT]
                # current topic comes before parent topic ALPHABETICALLY
                and l[current][cls.IND_TOPIC] < l[parent][cls.IND_TOPIC]
            ):
                l[current], l[parent] = l[parent], l[current]
            current = parent
        print("updated heap=", l)

    @classmethod
    def delete(cls, l: list[TupleCountTopic]) -> tuple:
        """Remove the top priority (FIFO)

        1. Heap structure must be complete tree (at all time)
        2. Root node must be the highest value
        3. Left child node is calculated such as -> 2*i+1 with i from 0 to len(l)-1
        4. Right child node is calculated such as -> 2*(i+1) with i from 0 to len(l)-1
        5. Parent node is calculated such as -> int(i/2)

        Args:
            l (list[TupleCountTopic]): Stack of element

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
                    left
                    if l[left][cls.IND_COUNT] > l[right][cls.IND_COUNT]
                    or (
                        l[left][cls.IND_COUNT] == l[right][cls.IND_COUNT]
                        # current topic comes before parent topic ALPHABETICALLY
                        and l[left][cls.IND_TOPIC] < l[right][cls.IND_TOPIC]
                    )
                    else right
                )
                # compare the current node with top_priority
                print(
                    f"> top priority is {'LEFT' if top_priority == left else 'RIGHT'}"
                )
                if l[top_priority][cls.IND_COUNT] > l[current][cls.IND_COUNT] or (
                    l[top_priority][cls.IND_COUNT] == l[current][cls.IND_COUNT]
                    # current topic comes before parent topic ALPHABETICALLY
                    and l[top_priority][cls.IND_TOPIC] < l[current][cls.IND_TOPIC]
                ):
                    print(">> swap")
                    l[top_priority], l[current] = l[current], l[top_priority]
                current = top_priority

            # if there is not right, it can have a left BUT if there is not left it MUST NOT have a right
            elif left < len(l):
                print("> only left leaf")
                # compare with its parent
                if l[left][cls.IND_COUNT] > l[current][cls.IND_COUNT] or (
                    l[left][cls.IND_COUNT] == l[current][cls.IND_COUNT]
                    # current topic comes before parent topic ALPHABETICALLY
                    and l[left][cls.IND_TOPIC] < l[current][cls.IND_TOPIC]
                ):
                    print(">> swap")
                    l[current], l[left] = l[left], l[current]
                current = left
            else:
                break
        print(f"{e} is deleted updated heap=", l)
        return e

    @classmethod
    def top_priority(cls, l: list[TupleCountTopic]) -> tuple:
        """FIFO - Return the most priority (far left) in queue without removing it

        Args:
            l (list[TupleCountTopic]): queue of element

        Returns:
            tuple: element
        """
        if len(l) == 0:
            raise IndexError("ERR: no top priority in empty Queue.")
        return l[0]

    @classmethod
    def sort(
        cls, l: list[TupleCountTopic], descending: bool = False
    ) -> list[TupleCountTopic]:
        """Sorting method"""
        print("START SORT", l)
        length = len(l)
        nl = [None] * length
        if descending:
            k = 0
            c = 1
        else:
            k = length - 1
            c = -1
        for i in range(length):
            nl[i * c + k] = cls.delete(l)
        print("END SORT", nl)
        return nl


if __name__ == "__main__":
    l = []
    MaxHeapWrapper.add(l, 15)
    MaxHeapWrapper.add(l, 25)
    MaxHeapWrapper.add(l, 28)
    MaxHeapWrapper.add(l, 1)
    MaxHeapWrapper.add(l, 21)
    MaxHeapWrapper.add(l, 53)
    MaxHeapWrapper.add(l, 33)
    MaxHeapWrapper.add(l, 8)
    MaxHeapWrapper.delete(l)
    l = MaxHeapWrapper.sort(l, True)
    print("FINAL", l)
