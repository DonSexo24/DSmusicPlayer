from typing import TypeVar, Union, Generic
from abc import ABC, abstractmethod
import os
import fnmatch


class ComparableValue(ABC):
    @abstractmethod
    def __lt__(self, other) -> bool:
        pass

    @abstractmethod
    def __gt__(self, other) -> bool:
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    @abstractmethod
    def __le__(self, other) -> bool:
        pass

    @abstractmethod
    def __ge__(self, other) -> bool:
        pass


T = TypeVar('T', bound=ComparableValue)
S = TypeVar('S', bound=Union['BinaryTree', 'CircularList', 'DoubleLinkedList', 'HashMap', 'LinkedList'])


# -------------------------------------------------------------------------------------------------------------------#

#        .--.
#       |o_o |
#       |:_/ |                                    #created by Juan Samuel Arbelaez & Juan Esteban Astaiza
#      //   \ \
#     (|     | )
#    /'\_   _/`\                                  #node
#    \___)=(___/


# -------------------------------------------------------------------------------------------------------------------#


class Node(Generic[T]):
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

    def __iter__(self):
        yield self.value


# -------------------------------------------------------------------------------------------------------------------#

#        .--.
#       |o_o |
#       |:_/ |                                    #created by Juan Samuel Arbelaez & Juan Esteban Astaiza
#      //   \ \
#     (|     | )                                  #DoublyLinkedList
#    /'\_   _/`\
#    \___)=(___/


# -------------------------------------------------------------------------------------------------------------------#

class DoubleLinkedList(Generic[T]):
    def __init__(self):
        self.__size = 0
        self.__sorted = False
        self._head = None

    def size(self):
        return self.__size

    def is_sorted(self):
        return self.__sorted

    def is_empty(self):
        return self.__size == 0

    def contains(self, value: T):
        node = self._head
        while node is not None:
            if node.value == value:
                return True
            node = node.next
        return False

    def add(self, index: int, value: T):
        if index < 0 or index > self.__size:
            raise IndexError("Index out of range")

        new_node = Node[T](value)
        if index == 0:
            new_node.next = self._head
            if self._head is not None:
                self._head.prev = new_node
            self._head = new_node
        else:
            node = self._head
            for i in range(index - 1):
                node = node.next
            new_node.next = node.next
            new_node.prev = node
            if node.next is not None:
                node.next.prev = new_node
            node.next = new_node

        self.__size += 1
        self.__sorted = False

    def append(self, value: T):
        self.add(self.__size, value)

    def remove(self, index: int):
        if index < 0 or index >= self.__size:
            raise IndexError("Index out of range")

        if index == 0:
            node = self._head
            self._head = node.next
            if self._head is not None:
                self._head.prev = None
        else:
            node = self._head
            for i in range(index):
                node = node.next
            node.prev.next = node.next
            if node.next is not None:
                node.next.prev = node.prev

        self.__size -= 1

    def remove_value(self, value: T):
        node = self._head
        index = 0
        while node is not None:
            if node.value == value:
                self.remove(index)
                return True
            node = node.next
            index += 1
        return False

    def poll(self, index: int):
        if index < 0 or index >= self.__size:
            raise IndexError("Index out of range")

        node = self._head
        for i in range(index):
            node = node.next

        self.remove(index)

        return node.value

    def sort(self):
        values = []
        node = self._head
        while node is not None:
            values.append(node.value)
            node = node.next

        values.sort()

        self.clear()

        for value in values:
            self.append(value)

        self.__sorted = True

    def insert(self, value: T):
        if not self.__sorted:
            raise ValueError("List must be sorted to use insert method")

        node = self._head
        index = 0
        while node is not None:
            if value <= node.value:
                self.add(index, value)
                return
            node = node.next
            index += 1

        self.append(value)

    def add_all(self, other_list):
        for value in other_list:
            self.append(value)

        self.__sorted = False

    def clear(self):
        self._head = None
        self.__size = 0

    def get(self, index: int):
        if index < 0 or index >= self.__size:
            raise IndexError("Index out of range")

        node = self._head
        for i in range(index):
            node = node.next

        return node.value

    def index_of(self, value: T):
        node = self._head
        index = 0
        while node is not None:
            if node.value == value:
                return index
            node = node.next
            index += 1
        return -1

    def last_index_of(self, value: T):
        node = self._head
        index = 0
        last_index = -1
        while node is not None:
            if node.value == value:
                last_index = index
            node = node.next
            index += 1
        return last_index

    def valid_index(self, index: int):
        return 0 <= index < self.__size

    def sub_list(self, start: int, end: int):
        if start < 0 or start >= self.__size:
            raise IndexError("Start index out of range")

        if end < 0 or end > self.__size:
            raise IndexError("End index out of range")

        if start > end:
            raise ValueError("Start index cannot be greater than end index")

        new_list = DoubleLinkedList[T]()
        node = self._head
        for i in range(start):
            node = node.next
        for i in range(start, end):
            new_list.append(node.value)
            node = node.next
        return new_list

    def remove_all(self, other_list):
        node = other_list._head
        while node is not None:
            self.remove_value(node.value)
            node = node.next

    def append_list(self, other_list):
        node = other_list._head
        while node is not None:
            self.append(node.value)
            node = node.next

    def __iter__(self):
        node = self._head
        while node is not None:
            yield node.value
            node = node.next


# -------------------------------------------------------------------------------------------------------------------#

#        .--.
#       |o_o |
#       |:_/ |                                    #created by Juan Samuel Arbelaez & Juan Esteban Astaiza
#      //   \ \
#     (|     | )                                  #Hashmap
#    /'\_   _/`\
#    \___)=(___/


# -------------------------------------------------------------------------------------------------------------------#

from typing import TypeVar, Generic

T = TypeVar('T')

class HashMap(Generic[T]):
    DEFAULT_CAPACITY = 16
    DEFAULT_LOAD_FACTOR = 0.75

    def __init__(self, capacity=DEFAULT_CAPACITY, load_factor=DEFAULT_LOAD_FACTOR):
        self.size = 0
        self.capacity = capacity
        self.load_factor = load_factor
        self.table = [None] * capacity

    def __iter__(self):
        for node in self.table:
            while node is not None:
                yield from node
                node = node.next

    def size(self):
        return self.size

    def isEmpty(self):
        return self.size == 0

    def contains_value(self, value: T):
        for node in self.table:
            while node is not None:
                if node.value == value:
                    return True
                node = node.next
        return False

    def contains_key(self, key):
        index = self.hash_of(key)
        node = self.table[index]
        while node is not None:
            if node.key == key:
                return True
            node = node.next
        return False

    def put_in(self, key, value: T):
        index = self.hash_of(key)
        node = self.table[index]
        while node is not None:
            if node.key == key:
                node.value = value
                return
            node = node.next
        new_node = Node[T](key, value)
        new_node.next = self.table[index]
        self.table[index] = new_node
        self.size += 1
        if self.size > self.capacity * self.load_factor:
            self.resize()

    def get(self, key):
        index = self.hash_of(key)
        node = self.table[index]
        while node is not None:
            if node.key == key:
                return node.value
            node = node.next
        return None

    def remove(self, key):
        index = self.hash_of(key)
        prev_node = None
        node = self.table[index]
        while node is not None:
            if node.key == key:
                if prev_node is None:
                    self.table[index] = node.next
                else:
                    prev_node.next = node.next
                self.size -= 1
                return node.value
            prev_node = node
            node = node.next
        return None

    def hash_of(self, key):
        return hash(key) % self.capacity

    def resize(self):
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity
        for node in self.table:
            while node is not None:
                index = self.hash_of(node.key)
                new_node = Node(node.key, node.value)
                new_node.next = new_table[index]
                new_table[index] = new_node
                node = node.next
        self.capacity = new_capacity
        self.table = new_table

    def add_all(self, other):
        for key in other:
            self.put_in(key, other[key])

    def clear(self):
        self.size = 0
        self.table = [None] * self.capacity

    def remove_all(self, other):
        for key in other:
            self.remove(key)

    def put(self, key, value: T):
        self.put_in(key, value)


# -------------------------------------------------------------------------------------------------------------------#

#        .--.
#       |o_o |
#       |:_/ |                                    #created by Juan Samuel Arbelaez & Juan Esteban Astaiza
#      //   \ \
#     (|     | )                                  #LinkedList
#    /'\_   _/`\
#    \___)=(___/


# -------------------------------------------------------------------------------------------------------------------#


class LinkedList(Generic[T]):
    def __init__(self):
        self._size = 0
        self._sorted = False
        self._head = None

    def size(self):
        return self._size

    def sorted(self):
        return self._sorted

    def isEmpty(self):
        return self._size == 0

    def contains(self, value: T):
        current = self._head
        while current:
            if current.value == value:
                return True
            current = current.next
        return False

    def add(self, index: int, value: T):
        if not self.validIndex(index):
            raise IndexError("Invalid index")
        if index == 0:
            self._head = Node(value, self._head)
        else:
            current = self._head
            for _ in range(index - 1):
                current = current.next
            current.next = Node(value, current.next)
        self._size += 1
        self._sorted = False

    def append(self, value: T):
        if self.isEmpty():
            self._head = Node[T](value)
        else:
            current = self._head
            while current.next:
                current = current.next
            current.next = Node[T](value)
        self._size += 1
        self._sorted = False

    def remove(self, index: int):
        if not self.validIndex(index):
            raise IndexError("Invalid index")
        if index == 0:
            self._head = self._head.next
        else:
            current = self._head
            for _ in range(index - 1):
                current = current.next
            current.next = current.next.next
        self._size -= 1

    def remove_by_value(self, value: T):
        if self.isEmpty():
            return
        if self._head.value == value:
            self._head = self._head.next
            self._size -= 1
            return
        current = self._head
        while current.next:
            if current.next.value == value:
                current.next = current.next.next
                self._size -= 1
                return
            current = current.next

    def poll(self, index: int):
        if not self.validIndex(index):
            raise IndexError("Invalid index")
        current = self._head
        for _ in range(index):
            current = current.next
        return current.value

    def sort(self):
        if self.isEmpty():
            return
        self._head = self._merge_sort(self._head)
        self._sorted = True

    def _merge_sort(self, head: 'Node'):
        if not head or not head.next:
            return head
        middle = self._get_middle(head)
        next_to_middle = middle.next
        middle.next = None
        left = self._merge_sort(head)
        right = self._merge_sort(next_to_middle)
        return self._sorted_merge(left, right)

    def _sorted_merge(self, a: 'Node', b: 'Node'):
        if not a:
            return b
        if not b:
            return a
        if a.value <= b.value:
            result = a
            result.next = self._sorted_merge(a.next, b)
        else:
            result = b
            result.next = self._sorted_merge(a, b.next)
        return result

    def _get_middle(self, head: 'Node'):
        if not head:
            return head
        slow = head
        fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    def insert(self, value: T):
        if not self._sorted:
            raise ValueError("List is not sorted")
        if self.isEmpty() or self._head.value >= value:
            self._head = Node(value, self._head)
            self._size += 1
            return
        current = self._head
        while current.next and current.next.value < value:
            current = current.next
        current.next = Node(value, current.next)
        self._size += 1

    def addAll(self, other: S):
        for value in other:
            self.append(value)

    def clear(self):
        self._head = None
        self._size = 0
        self._sorted = False

    def get(self, index: int):
        return self.poll(index)

    def indexOf(self, value: T):
        index = 0
        current = self._head
        while current:
            if current.value == value:
                return index
            current = current.next
            index += 1
        return -1

    def lastIndexOf(self, value: T):
        index = 0
        last_index = -1
        current = self._head
        while current:
            if current.value == value:
                last_index = index
            current = current.next
            index += 1
        return last_index

    def validIndex(self, index: int):
        return 0 <= index <= self._size

    def subList(self, start: int, end: int):
        if not self.validIndex(start) or not self.validIndex(end) or start > end:
            raise IndexError("Invalid index")
        sub_list = LinkedList()
        current = self._head
        for i in range(start):
            current = current.next
        for _ in range(end - start):
            sub_list.append(current.value)
            current = current.next
        return sub_list

    def removeAll(self, other: S):
        for value in other:
            while self.contains(value):
                self.remove_by_value(value)

    def appendList(self, other: S):
        self.addAll(other)

    def __iter__(self):
        current = self._head
        while current:
            yield current.value
            current = current.next


# -------------------------------------------------------------------------------------------------------------------#

#        .--.
#       |o_o |
#       |:_/ |                                    #created by Juan Samuel Arbelaez & Juan Esteban Astaiza
#      //   \ \
#     (|     | )
#    /'\_   _/`\                                  #Queue
#    \___)=(___/


# -------------------------------------------------------------------------------------------------------------------#

class Queue:
    def __init__(self):
        self.__size = 0
        self.__head = None

    def size(self):
        return self.__size

    def is_empty(self):
        return self.__size == 0

    def contains(self, value):
        current = self.__head
        while current:
            if current.value == value:
                return True
            current = current.next
        return False

    def push(self, value):
        node = Node(value)
        if self.__head is None:
            self.__head = node
        else:
            current = self.__head
            while current.next:
                current = current.next
            current.next = node
        self.__size += 1

    def poll(self):
        if self.__head is None:
            raise IndexError("Queue is empty")
        value = self.__head.value
        self.__head = self.__head.next
        self.__size -= 1
        return value

    def remove(self, value):
        if self.__head is None:
            raise ValueError("Value not found")
        if self.__head.value == value:
            self.__head = self.__head.next
            self.__size -= 1
            return
        current = self.__head
        while current.next:
            if current.next.value == value:
                current.next = current.next.next
                self.__size -= 1
                return
            current = current.next
        raise ValueError("Value not found")

    def peek(self):
        if self.__head is None:
            raise IndexError("Queue is empty")
        return self.__head.value

    def insert(self, index, value):
        if index < 0 or index > self.__size:
            raise IndexError("Index out of range")
        if index == 0:
            node = Node(value)
            node.next = self.__head
            self.__head = node
            self.__size += 1
            return
        current = self.__head
        for i in range(index - 1):
            current = current.next
        node = Node(value)
        node.next = current.next
        current.next = node
        self.__size += 1

    def add_all(self, values):
        for value in values:
            self.push(value)

    def clear(self):
        self.__size = 0
        self.__head = None

    def index_of(self, value):
        current = self.__head
        index = 0
        while current:
            if current.value == value:
                return index
            current = current.next
            index += 1
        raise ValueError("Value not found")

    def last_index_of(self, value):
        current = self.__head
        index = -1
        i = 0
        while current:
            if current.value == value:
                index = i
            current = current.next
            i += 1
        if index == -1:
            raise ValueError("Value not found")
        return index

    def valid_index(self, index):
        return 0 <= index < self.__size

    def sub_queue(self, start_index, end_index):
        if start_index < 0 or end_index > self.__size or start_index > end_index:
            raise IndexError("Index out of range")
        current = self.__head
        for i in range(start_index):
            current = current.next
        result = Queue()
        for i in range(start_index, end_index):
            result.push(current.value)
            current = current.next
        return result

    def remove_all(self, values):
        current = self.__head
        previous = None
        count = 0
        while current:
            if current.value in values:
                if previous is None:
                    self.__head = current.next
                else:
                    previous.next = current.next
                count += 1
                self.__size -= 1
            else:
                previous = current
            current = current.next
        return count

    def append_queue(self, other):
        for value in other:
            self.push(value)

    def __iter__(self):
        current = self.__head
        while current:
            yield current.value
            current = current.next


# -------------------------------------------------------------------------------------------------------------------#

#        .--.
#       |o_o |
#       |:_/ |                                    #created by Juan Samuel Arbelaez & Juan Esteban Astaiza
#      //   \ \
#     (|     | )                                  #Stack
#    /'\_   _/`\
#    \___)=(___/


# -------------------------------------------------------------------------------------------------------------------#

class Stack:
    def __init__(self):
        self.__size = 0
        self.__top = None

    def size(self):
        return self.__size

    def is_empty(self):
        return self.__size == 0

    def contains(self, value):
        current = self.__top
        while current is not None:
            if current.value == value:
                return True
            current = current.next
        return False

    def push(self, value):
        new_node = Node(value)
        new_node.next = self.__top
        self.__top = new_node
        self.__size += 1

    def poll(self):
        if self.__top is None:
            return None
        value = self.__top.value
        self.__top = self.__top.next
        self.__size -= 1
        return value

    def remove(self, value):
        prev = None
        current = self.__top
        while current is not None:
            if current.value == value:
                if prev is None:
                    self.__top = current.next
                else:
                    prev.next = current.next
                self.__size -= 1
                return True
            prev = current
            current = current.next
        return False

    def peek(self):
        if self.__top is None:
            return None
        return self.__top.value

    def insert(self, index, value):
        if index < 0 or index > self.__size:
            raise IndexError("Index out of range")
        new_node = Node(value)
        if index == 0:
            new_node.next = self.__top
            self.__top = new_node
        else:
            current = self.__top
            for i in range(index - 1):
                current = current.next
            new_node.next = current.next
            current.next = new_node
        self.__size += 1

    def add_all(self, iterable):
        for value in iterable:
            self.push(value)

    def clear(self):
        self.__size = 0
        self.__top = None

    def index_of(self, value):
        current = self.__top
        index = 0
        while current is not None:
            if current.value == value:
                return index
            current = current.next
            index += 1
        return -1

    def last_index_of(self, value):
        current = self.__top
        index = -1
        last_index = -1
        while current is not None:
            if current.value == value:
                last_index = index
            current = current.next
            index += 1
        return last_index

    def valid_index(self, index):
        return 0 <= index < self.__size

    def sub_list(self, start, end=None):
        if start < 0 or start >= self.__size:
            raise IndexError("Start index out of range")
        if end is None:
            end = self.__size
        if end < 0 or end > self.__size:
            raise IndexError("End index out of range")
        if start > end:
            raise IndexError("Start index greater than end index")
        result = Stack()
        current = self.__top
        for i in range(end):
            if i >= start:
                result.push(current.value)
            current = current.next
        return result

    def remove_all(self, iterable):
        count = 0
        for value in iterable:
            while self.remove(value):
                count += 1
        return count

    def append_list(self, iterable):
        for value in iterable:
            self.push(value)

    def __iter__(self):
        current = self.__top
        while current is not None:
            yield current.value
            current = current.next


# -------------------------------------------------------------------------------------------------------------------#

#        .--.
#       |o_o |
#       |:_/ |                                    #created by Juan Samuel Arbelaez & Juan Esteban Astaiza
#      //   \ \
#     (|     | )
#    /'\_   _/`\                                  #Hard drive search
#    \___)=(___/


# -------------------------------------------------------------------------------------------------------------------#

directory = "C:\\"

pattern = "*.mp3"

for root, dirs, files in os.walk(directory):
    for filename in fnmatch.filter(files, pattern):
        print(os.path.join(root, filename))


# -------------------------------------------------------------------------------------------------------------------#

#        .--.
#       |o_o |
#       |:_/ |                                    #created by Juan Samuel Arbelaez & Juan Esteban Astaiza
#      //   \ \
#     (|     | )                                  #Binary tree
#    /'\_   _/`\
#    \___)=(___/


# -------------------------------------------------------------------------------------------------------------------#

class BinaryTree(Generic[T]):

    def __init__(self):
        self.__height = 0
        self.__weight = 0
        self.__root = None

    def __check_type(self, value: T):
        if not all(hasattr(value, attr) for attr in ('__lt__', '__gt__', '__eq__', '__le__', '__ge__')):
            raise TypeError("BinaryTree can only store objects that implement comparison operators.")

    def height(self):
        return self.__height

    def weight(self):
        return self.__weight

    def is_empty(self):
        return self.__root is None

    def contains(self, value: T):
        return self.__contains_helper(self.__root, value)

    def __contains_helper(self, node: 'Node[T]', value: T):
        if node is None:
            return False
        elif value == node.value:
            return True
        elif value < node.value:
            return self.__contains_helper(node.left, value)
        else:
            return self.__contains_helper(node.right, value)

    def add(self, value: T):
        self.__check_type(value)
        if self.__root is None:
            self.__root = Node[T](value)
        else:
            self.__add_helper(self.__root, value)
        self.__weight += 1

    def __add_helper(self, node: 'Node[T]', value: T):
        if value == node.value:
            raise AttributeError("Tree already contains value: {value}")
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self.__add_helper(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self.__add_helper(node.right, value)

    def balance(self):
        values = self.in_order_traversal()
        self.clear()
        self.__balance_helper(values, 0, len(values) - 1)

    def __balance_helper(self, values: [T], start: int, end: int):
        if start > end:
            return None
        mid = (start + end) // 2
        self.add(values[mid])
        self.__balance_helper(values, start, mid - 1)
        self.__balance_helper(values, mid + 1, end)

    def remove(self, value: T):
        self.__root = self.__remove_helper(self.__root, value)

    def __remove_helper(self, node: 'Node[T]', value: T):
        if node is None:
            return None
        elif value < node.value:
            node.left = self.__remove_helper(node.left, value)
        elif value > node.value:
            node.right = self.__remove_helper(node.right, value)
        else:
            if node.left is None and node.right is None:
                return None
            elif node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                successor = self.__find_min(node.right)
                node.value = successor.value
                node.right = self.__remove_helper(node.right, successor.value)
        return node

    def __find_min(self, node: 'Node[T]'):
        while node.left is not None:
            node = node.left
        return node

    def clear(self):
        self.__root = None

    def in_order_traversal(self):
        values = []
        self.__in_order_traversal_helper(self.__root, values)
        return values

    def __in_order_traversal_helper(self, node: 'Node[T]', values: [ComparableValue]):
        if node is not None:
            self.__in_order_traversal_helper(node.left, values)
            values.append(node.value)
            self.__in_order_traversal_helper(node.right, values)

    def post_order_traversal(self):
        values = []
        self.__post_order_traversal_helper(self.__root, values)
        return values

    def __post_order_traversal_helper(self, node: 'Node[T]', values: [ComparableValue]):
        if node is not None:
            self.__post_order_traversal_helper(node.left, values)
            self.__post_order_traversal_helper(node.right, values)
            values.append(node.value)

    def pre_order_traversal(self):
        values = []
        self.__pre_order_traversal_helper(self.__root, values)
        return values

    def __pre_order_traversal_helper(self, node: 'Node[T]', values: [ComparableValue]):
        if node is not None:
            values.append(node.value)
            self.__pre_order_traversal_helper(node.left, values)
            self.__pre_order_traversal_helper(node.right, values)


# -------------------------------------------------------------------------------------------------------------------#

#        .--.
#       |o_o |
#       |:_/ |                                    #created by Juan Samuel Arbelaez & Juan Esteban Astaiza
#      //   \ \
#     (|     | )                                  #Circular list
#    /'\_   _/`\
#    \___)=(___/


# -------------------------------------------------------------------------------------------------------------------#

class Node(Generic[T]):
    def __init__(self, value: T, next=None):
        self.value = value
        self.next = next


class CircularList(Generic[T]):
    def __init__(self):
        self.__sorted_by = None
        self.__size = 0
        self.__sorted = False
        self.__head = None

    def size(self):
        return self.__size

    def is_sorted(self):
        return self.__sorted

    def is_empty(self):
        return self.__size == 0

    def get_sort_key(self):
        return self.__sorted_by

    def contains(self, value: T):
        current = self.__head
        for i in range(self.__size):
            if current.value == value:
                return True
            current = current.next
        return False

    def add(self, index: int, value: T):
        if index < 0 or index > self.__size:
            raise IndexError("Index out of range")
        new_node = Node(value)
        if index == 0:
            if self.__head is None:
                new_node.next = new_node
                self.__head = new_node
            else:
                new_node.next = self.__head
                current = self.__head
                while current.next != self.__head:
                    current = current.next
                current.next = new_node
                self.__head = new_node
        else:
            current = self.__head
            for i in range(index - 1):
                current = current.next
            new_node.next = current.next
            current.next = new_node
        self.__size += 1
        self.__sorted = False

    def append(self, value: T):
        self.add(self.__size, value)

    def remove(self, index: int):
        if index < 0 or index >= self.__size:
            raise IndexError("Index out of range")
        if index == 0:
            if self.__size == 1:
                self.__head = None
            else:
                current = self.__head
                while current.next != self.__head:
                    current = current.next
                self.__head = self.__head.next
                current.next = self.__head
        else:
            current = self.__head
            for i in range(index - 1):
                current = current.next
            current.next = current.next.next
        self.__size -= 1
        self.__sorted = False

    def remove_value(self, value: T):
        current = self.__head
        for i in range(self.__size):
            if current.value == value:
                self.remove(i)
                return True
            current = current.next
            self.__sorted = False
        return False

    def poll(self, index: int):
        if index < 0 or index >= self.__size:
            raise IndexError("Index out of range")
        current = self.__head
        for i in range(index - 1):
            current = current.next
        value = current.next.value
        self.remove(index)
        return value

    def sort(self, key):
        if self.__sorted and self.__sorted_by == key:
            return

        if key is None:
            key = lambda x: x

        # convert string key to attribute getter function
        if isinstance(key, str):
            key = lambda x: getattr(x, key)
        else:
            raise AttributeError("Attribute {key} not found")

        # convert list to tuple to prevent modification during sorting
        nodes = tuple(self)

        # use key function to sort nodes
        nodes = sorted(nodes, key=key)

        # rebuild list from sorted nodes
        self.__head = None
        for node in nodes:
            self.append(node.value)

        self.__sorted = True
        self.__sorted_by = key if not isinstance(key, str) else None

    def insert(self, value: T):
        if self.__sorted:
            current = self.__head
            index = 0
            while index < self.__size and current.value <= value:
                current = current.next
                index += 1
            self.add(index, value)
            self.__sorted = False
        else:
            raise Exception("Cannot insert into unsorted list")

    def add_all(self, other: S):
        for value in other:
            self.append(value)

    def clear(self):
        self.__head = None
        self.__size = 0
        self.__sorted = False
        self.__sorted_by = None

    def get(self, index: int):
        if index < 0 or index >= self.__size:
            raise IndexError("Index out of range")
        current = self.__head
        for i in range(index):
            current = current.next
        return current.value

    def index_of(self, value: T):
        current = self.__head
        for i in range(self.__size):
            if current.value == value:
                return i
            current = current.next
        return -1

    def last_index_of(self, value: T):
        current = self.__head
        last_index = -1
        for i in range(self.__size):
            if current.value == value:
                last_index = i
            current = current.next
        return last_index

    def valid_index(self, index: int):
        return 0 <= index < self.__size

    def sub_list(self, start: int, end: int):
        if start < 0 or end > self.__size or start >= end:
            raise ValueError("Invalid start or end index")
        sub_list = CircularList()
        current = self.__head
        for i in range(start):
            current = current.next
        for i in range(start, end):
            sub_list.append(current.value)
            current = current.next
        return sub_list

    def remove_all(self, value: T):
        current = self.__head
        prev = None
        removed_count = 0
        while current is not None:
            if current.value == value:
                if prev is None:
                    self.__head = current.next
                else:
                    prev.next = current.next
                self.__size -= 1
                removed_count += 1
            else:
                prev = current
            current = current.next
            self.__sorted = False
        return removed_count

    def append_list(self, other: S):
        if other is None or other.is_empty():
            return
        current = other.__head
        for i in range(other.__size):
            self.append(current.value)
            current = current.next

    def __iter__(self):
        current = self.__head
        while True:
            yield current.value
            current = current.next
            if current == self.__head:
                break
