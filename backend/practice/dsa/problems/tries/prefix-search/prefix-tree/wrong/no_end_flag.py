class PrefixTree:
    # Mistake: search() accepts any path that exists, so prefixes of stored words count as words.
    def __init__(self):
        self.root = {}

    def insert(self, word):
        node = self.root
        for c in word:
            node = node.setdefault(c, {})

    def _walk(self, s):
        node = self.root
        for c in s:
            node = node.get(c)
            if node is None:
                return None
        return node

    def search(self, word):
        return self._walk(word) is not None

    def startsWith(self, prefix):
        return self._walk(prefix) is not None
