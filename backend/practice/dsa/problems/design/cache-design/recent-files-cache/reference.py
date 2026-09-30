class _Node:
    __slots__ = ("key", "size", "prev", "next")

    def __init__(self, key=0, size=0):
        self.key, self.size, self.prev, self.next = key, size, None, None


class RecentFilesCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.nodes = {}
        self.head, self.tail = _Node(), _Node()  # head.next = most recent, tail.prev = oldest
        self.head.next, self.tail.prev = self.tail, self.head

    def _unlink(self, node):
        node.prev.next, node.next.prev = node.next, node.prev

    def _push_front(self, node):
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    def open(self, fileId):
        node = self.nodes.get(fileId)
        if node is None:
            return -1
        self._unlink(node)
        self._push_front(node)
        return node.size

    def save(self, fileId, size):
        node = self.nodes.get(fileId)
        if node is not None:
            node.size = size
            self._unlink(node)
        else:
            if len(self.nodes) == self.capacity:
                oldest = self.tail.prev
                self._unlink(oldest)
                del self.nodes[oldest.key]
            node = _Node(fileId, size)
            self.nodes[fileId] = node
        self._push_front(node)
