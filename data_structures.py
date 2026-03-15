"""
Part 2: Elementary Data Structures Implementation
===================================================
Implements the following data structures from scratch:
1. Dynamic Array with basic matrix support
2. Stack (array-based)
3. Queue (array-based, circular buffer)
4. Singly Linked List
5. (Bonus) Rooted Tree using linked nodes

Author: Aashish
Course: CS Master's Program - University of the Cumberlands
Assignment: 6 - Medians and Order Statistics & Elementary Data Structures
"""


# =============================================================================
# 1. Dynamic Array
# =============================================================================

class DynamicArray:
    """
    A resizable array that doubles capacity when full and halves when quarter-full.

    Time Complexities:
        - Access by index: O(1)
        - Append (amortized): O(1)
        - Insert at index: O(n)
        - Delete at index: O(n)
        - Search: O(n)
    """

    def __init__(self, capacity=4):
        """Initialize with a given starting capacity."""
        self._capacity = max(capacity, 1)
        self._size = 0
        self._data = [None] * self._capacity

    def __len__(self):
        return self._size

    def __getitem__(self, index):
        """Access element at index. O(1)."""
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of range for size {self._size}.")
        return self._data[index]

    def __setitem__(self, index, value):
        """Set element at index. O(1)."""
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of range for size {self._size}.")
        self._data[index] = value

    def __repr__(self):
        return f"DynamicArray({[self._data[i] for i in range(self._size)]})"

    def _resize(self, new_capacity):
        """Resize the internal storage. O(n)."""
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_capacity

    def append(self, value):
        """Add element to the end. Amortized O(1)."""
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        self._data[self._size] = value
        self._size += 1

    def insert(self, index, value):
        """Insert element at index, shifting subsequent elements right. O(n)."""
        if index < 0 or index > self._size:
            raise IndexError(f"Insert index {index} out of range.")
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        # Shift elements right
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        self._data[index] = value
        self._size += 1

    def delete(self, index):
        """Remove element at index, shifting subsequent elements left. O(n)."""
        if index < 0 or index >= self._size:
            raise IndexError(f"Delete index {index} out of range.")
        removed = self._data[index]
        # Shift elements left
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        self._data[self._size - 1] = None
        self._size -= 1
        # Shrink if quarter full
        if self._size > 0 and self._size <= self._capacity // 4:
            self._resize(self._capacity // 2)
        return removed

    def search(self, value):
        """Return index of first occurrence, or -1 if not found. O(n)."""
        for i in range(self._size):
            if self._data[i] == value:
                return i
        return -1


# =============================================================================
# 2. Matrix (2D Array)
# =============================================================================

class Matrix:
    """
    A 2D matrix implemented using a flat array for cache efficiency.

    Time Complexities:
        - Access/Set element: O(1)
        - Row/Column retrieval: O(cols) / O(rows)
    """

    def __init__(self, rows, cols, default=0):
        self._rows = rows
        self._cols = cols
        self._data = [default] * (rows * cols)

    def get(self, row, col):
        """Access element at (row, col). O(1)."""
        self._check_bounds(row, col)
        return self._data[row * self._cols + col]

    def set(self, row, col, value):
        """Set element at (row, col). O(1)."""
        self._check_bounds(row, col)
        self._data[row * self._cols + col] = value

    def _check_bounds(self, row, col):
        if row < 0 or row >= self._rows or col < 0 or col >= self._cols:
            raise IndexError(f"({row}, {col}) out of bounds for {self._rows}x{self._cols} matrix.")

    @property
    def shape(self):
        return (self._rows, self._cols)

    def __repr__(self):
        rows = []
        for r in range(self._rows):
            row = [str(self._data[r * self._cols + c]) for c in range(self._cols)]
            rows.append("[" + ", ".join(row) + "]")
        return "Matrix([\n  " + "\n  ".join(rows) + "\n])"


# =============================================================================
# 3. Stack (Array-Based)
# =============================================================================

class Stack:
    """
    LIFO Stack implemented using a Python list as backing array.

    Time Complexities:
        - Push: O(1) amortized
        - Pop: O(1)
        - Peek: O(1)
        - is_empty: O(1)
    """

    def __init__(self):
        self._data = []

    def push(self, value):
        """Push element onto the stack. O(1) amortized."""
        self._data.append(value)

    def pop(self):
        """Remove and return the top element. O(1)."""
        if self.is_empty():
            raise IndexError("Pop from an empty stack.")
        return self._data.pop()

    def peek(self):
        """Return the top element without removing it. O(1)."""
        if self.is_empty():
            raise IndexError("Peek on an empty stack.")
        return self._data[-1]

    def is_empty(self):
        """Check if the stack is empty. O(1)."""
        return len(self._data) == 0

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return f"Stack(top -> {list(reversed(self._data))})"


# =============================================================================
# 4. Queue (Array-Based Circular Buffer)
# =============================================================================

class Queue:
    """
    FIFO Queue implemented as a circular buffer for O(1) enqueue/dequeue.

    Time Complexities:
        - Enqueue: O(1) amortized
        - Dequeue: O(1)
        - Peek: O(1)
        - is_empty: O(1)
    """

    def __init__(self, capacity=4):
        self._capacity = max(capacity, 1)
        self._data = [None] * self._capacity
        self._front = 0
        self._size = 0

    def enqueue(self, value):
        """Add element to the rear. O(1) amortized."""
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        rear = (self._front + self._size) % self._capacity
        self._data[rear] = value
        self._size += 1

    def dequeue(self):
        """Remove and return the front element. O(1)."""
        if self.is_empty():
            raise IndexError("Dequeue from an empty queue.")
        value = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        # Shrink if quarter full
        if self._size > 0 and self._size <= self._capacity // 4:
            self._resize(self._capacity // 2)
        return value

    def peek(self):
        """Return the front element without removing it. O(1)."""
        if self.is_empty():
            raise IndexError("Peek on an empty queue.")
        return self._data[self._front]

    def is_empty(self):
        """Check if the queue is empty. O(1)."""
        return self._size == 0

    def _resize(self, new_capacity):
        """Resize the circular buffer. O(n)."""
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[(self._front + i) % self._capacity]
        self._data = new_data
        self._front = 0
        self._capacity = new_capacity

    def __len__(self):
        return self._size

    def __repr__(self):
        items = [self._data[(self._front + i) % self._capacity] for i in range(self._size)]
        return f"Queue(front -> {items})"


# =============================================================================
# 5. Singly Linked List
# =============================================================================

class _SLLNode:
    """Node for Singly Linked List."""
    __slots__ = ('value', 'next')

    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node


class SinglyLinkedList:
    """
    Singly Linked List with insertion, deletion, search, and traversal.

    Time Complexities:
        - Insert at head: O(1)
        - Insert at tail: O(n)  [O(1) with tail pointer maintained]
        - Delete by value: O(n)
        - Search: O(n)
        - Traversal: O(n)
    """

    def __init__(self):
        self._head = None
        self._size = 0

    def insert_head(self, value):
        """Insert a new node at the head. O(1)."""
        self._head = _SLLNode(value, self._head)
        self._size += 1

    def insert_tail(self, value):
        """Insert a new node at the tail. O(n)."""
        new_node = _SLLNode(value)
        if self._head is None:
            self._head = new_node
        else:
            current = self._head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self._size += 1

    def delete(self, value):
        """Delete the first node with the given value. O(n). Returns True if found."""
        if self._head is None:
            return False
        if self._head.value == value:
            self._head = self._head.next
            self._size -= 1
            return True
        current = self._head
        while current.next is not None:
            if current.next.value == value:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        return False

    def search(self, value):
        """Return True if value exists in the list. O(n)."""
        current = self._head
        while current is not None:
            if current.value == value:
                return True
            current = current.next
        return False

    def traverse(self):
        """Return all elements as a Python list. O(n)."""
        result = []
        current = self._head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result

    def __len__(self):
        return self._size

    def __repr__(self):
        return f"SinglyLinkedList({' -> '.join(str(x) for x in self.traverse())})"


# =============================================================================
# 6. Rooted Tree (Bonus - using linked nodes)
# =============================================================================

class TreeNode:
    """Node for a general rooted tree (each node has a list of children)."""
    __slots__ = ('value', 'children')

    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child_node):
        """Add a child to this node. O(1)."""
        self.children.append(child_node)


class RootedTree:
    """
    General rooted tree implemented with linked nodes.

    Each node can have an arbitrary number of children.
    Supports DFS and BFS traversal.
    """

    def __init__(self, root_value):
        self.root = TreeNode(root_value)

    def dfs(self, node=None):
        """Depth-first traversal. O(n)."""
        if node is None:
            node = self.root
        result = [node.value]
        for child in node.children:
            result.extend(self.dfs(child))
        return result

    def bfs(self):
        """Breadth-first traversal using a simple list-based queue. O(n)."""
        result = []
        queue = [self.root]
        while queue:
            current = queue.pop(0)
            result.append(current.value)
            queue.extend(current.children)
        return result

    def __repr__(self):
        return f"RootedTree(root={self.root.value}, dfs={self.dfs()})"


# =============================================================================
# Demonstration / Verification
# =============================================================================

def demo_data_structures():
    """Demonstrate all data structures with example operations."""

    print("=" * 60)
    print("DYNAMIC ARRAY DEMO")
    print("=" * 60)
    da = DynamicArray()
    for v in [10, 20, 30, 40, 50]:
        da.append(v)
    print(f"  After appending 10-50: {da}")
    da.insert(2, 25)
    print(f"  After insert(2, 25):   {da}")
    removed = da.delete(0)
    print(f"  After delete(0):       {da}  (removed {removed})")
    print(f"  Search for 30:         index {da.search(30)}")
    print(f"  Search for 99:         index {da.search(99)}")

    print()
    print("=" * 60)
    print("MATRIX DEMO")
    print("=" * 60)
    m = Matrix(3, 3)
    for i in range(3):
        for j in range(3):
            m.set(i, j, i * 3 + j + 1)
    print(f"  {m}")
    print(f"  Element at (1,2): {m.get(1, 2)}")

    print()
    print("=" * 60)
    print("STACK DEMO")
    print("=" * 60)
    s = Stack()
    for v in [1, 2, 3, 4, 5]:
        s.push(v)
    print(f"  After pushing 1-5: {s}")
    print(f"  Pop: {s.pop()}")
    print(f"  Peek: {s.peek()}")
    print(f"  After pop: {s}")

    print()
    print("=" * 60)
    print("QUEUE DEMO")
    print("=" * 60)
    q = Queue()
    for v in ["A", "B", "C", "D"]:
        q.enqueue(v)
    print(f"  After enqueue A-D: {q}")
    print(f"  Dequeue: {q.dequeue()}")
    print(f"  Peek: {q.peek()}")
    print(f"  After dequeue: {q}")

    print()
    print("=" * 60)
    print("SINGLY LINKED LIST DEMO")
    print("=" * 60)
    sll = SinglyLinkedList()
    for v in [10, 20, 30]:
        sll.insert_tail(v)
    sll.insert_head(5)
    print(f"  After inserts:    {sll}")
    sll.delete(20)
    print(f"  After delete(20): {sll}")
    print(f"  Search 30: {sll.search(30)}")
    print(f"  Search 99: {sll.search(99)}")

    print()
    print("=" * 60)
    print("ROOTED TREE DEMO")
    print("=" * 60)
    tree = RootedTree("CEO")
    vp1 = TreeNode("VP Engineering")
    vp2 = TreeNode("VP Sales")
    dev1 = TreeNode("Dev Team Lead")
    dev2 = TreeNode("QA Team Lead")
    vp1.add_child(dev1)
    vp1.add_child(dev2)
    tree.root.add_child(vp1)
    tree.root.add_child(vp2)
    print(f"  DFS: {tree.dfs()}")
    print(f"  BFS: {tree.bfs()}")


if __name__ == "__main__":
    demo_data_structures()
