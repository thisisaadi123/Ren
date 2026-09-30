# Correct but O(capacity) per call: too slow for the largest caches.
class RecentFilesCache:
    # A plain list ordered from oldest to newest: O(capacity) per call, obviously right.
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []  # [fileId, size]

    def _find(self, fileId):
        for i, (k, _) in enumerate(self.items):
            if k == fileId:
                return i
        return -1

    def open(self, fileId):
        i = self._find(fileId)
        if i < 0:
            return -1
        item = self.items.pop(i)
        self.items.append(item)
        return item[1]

    def save(self, fileId, size):
        i = self._find(fileId)
        if i >= 0:
            self.items.pop(i)
        elif len(self.items) == self.capacity:
            self.items.pop(0)
        self.items.append([fileId, size])
