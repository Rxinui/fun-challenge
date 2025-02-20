from abc import ABC, abstractmethod

type IntStr = tuple[int, str]


class HeapBinome[IntStr](ABC):

    IND_COUNT = 0
    IND_TOPIC = 1

    @classmethod
    @abstractmethod
    def has_priority_over(cls, t1: IntStr, t2: IntStr) -> bool:
        """Compare t1 with t2 and return whether t1 has over priority over t2

        Args:
            t1 (IntStr): to compare
            t2 (IntStr): compared with

        Returns:
            bool: True if t1 more priority than t2 else False
        """
        pass

    @classmethod
    def add(cls, l: list[IntStr], e: IntStr) -> None:
        """Add $e to the heap respecting the following:

        1. Heap structure must be complete tree (at all time)
        2. Root node must be the most priority value
        3. Left child node is calculated such as -> 2*i+1
        4. Right child node is calculated such as -> 2*(i+1)
        5. Parent node is calculated such as -> int(i/2)

        Args:
            l (list[str]): heap
            e (str): element
        """
        get_parent = lambda ind: int(ind / 2)
        # NOTE concatenation create new list out of two list -> o(k+n) ≈ O(n)
        # Add element to the end, respect complete tree
        l.append(e)
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
    def delete(cls, l: list[IntStr]) -> IntStr:
        """Remove the root respecting the follwing:

        1. Heap structure must be complete tree (at all time)
        2. Root node must be the most priority value
        3. Left child node is calculated such as -> 2*i+1
        4. Right child node is calculated such as -> 2*(i+1)
        5. Parent node is calculated such as -> int(i/2)

        Args:
            l (list[IntStr]): heap

        Returns:
            IntStr: element
        """
        get_left = lambda i: 2 * i + 1
        get_right = lambda i: 2 * (i + 1)
        current = 0
        # Last element become root then root is deleted
        l[0], l[-1] = l[-1], l[0]
        e = l.pop()
        # we compare the root down to the leaf
        # while there is a leaf available to be compared with
        while current < len(l):
            left = get_left(current)
            right = get_right(current)
            print(f">  heap={l} current={current} left={left} right={right}")
            if left < len(l) and right < len(l):
                print("> left and right leaves")
                # take the top priority between sibling to get the direction to leaf
                top_priority = (
                    left if cls.has_priority_over(l[left], l[right]) else right
                )
                # compare the current node with top_priority
                if cls.has_priority_over(l[top_priority], l[current]):
                    print(">> swap")
                    l[top_priority], l[current] = l[current], l[top_priority]
                current = top_priority
            # if there is not right, it can have a left
            elif left < len(l):
                print("> only left leaf")
                # compare current with its left child
                if cls.has_priority_over(l[left], l[current]):
                    print(">> swap")
                    l[current], l[left] = l[left], l[current]
                current = left
            else:
                break
        print(f"{e} is deleted updated heap=", l)
        return e

    @classmethod
    def first_out(cls, l: list[IntStr]) -> IntStr:
        """FIFO - Return the most priority (far left) in queue without removing it

        Args:
            l (list[IntStr]): queue of element

        Returns:
            IntStr: element
        """
        if len(l) == 0:
            raise IndexError("ERR: no top priority in empty Queue.")
        return l[0]

    @classmethod
    def sort(cls, l: list[IntStr]) -> list[IntStr]:
        """Heapsort

        Args:
            l (list[IntStr]): heap
        Returns:
            list[IntStr]: sorted heap
        """
        if len(l) > 0:
            e = cls.delete(l)
            cls.sort(l)
            l.append(e)
        return l


class MinHeapBinome[IntStr](HeapBinome):
    """Interpret a list as heap:
    Reading from 0 to len(list) ->  Breadth-First Traversal (from root, level by level)
    Small values -> Big values
    """

    @classmethod
    def has_priority_over(cls, t1: IntStr, t2: IntStr) -> bool:
        """Compare t1 '<' t2 and return whether t1 has priority over t2

        Args:
            t1 (IntStr): to compare
            t2 (IntStr): compared with

        Returns:
            bool: True if t1 < t2 else False
        """
        return t1[cls.IND_COUNT] < t2[cls.IND_COUNT] or (
            t1[cls.IND_COUNT] == t2[cls.IND_COUNT]
            # current topic comes before parent topic ALPHABETICALLY
            and t1[cls.IND_TOPIC] > t2[cls.IND_TOPIC]
        )

    @classmethod
    def add(cls, l: list[IntStr], e: IntStr) -> None:
        super().add(l, e)

    @classmethod
    def delete(cls, l: list[IntStr]) -> IntStr:
        return super().delete(l)

    @classmethod
    def first_out(cls, l: list[IntStr]) -> IntStr:
        return super().first_out(l)

    @classmethod
    def sort(cls, l: list[IntStr]) -> list[IntStr]:
        return super().sort(l)
