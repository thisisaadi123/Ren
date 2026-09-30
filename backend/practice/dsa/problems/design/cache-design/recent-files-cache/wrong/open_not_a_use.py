class RecentFilesCache:
    # Mistake: opening a file doesn't refresh it, so eviction order is by save time only.
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = {}

    def open(self, fileId):
        return self.items.get(fileId, -1)

    def save(self, fileId, size):
        if fileId in self.items:
            del self.items[fileId]
        elif len(self.items) == self.capacity:
            del self.items[next(iter(self.items))]
        self.items[fileId] = size
