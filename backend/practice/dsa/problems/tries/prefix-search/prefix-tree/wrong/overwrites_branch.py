class PrefixTree:
    # Mistake: inserting a word replaces the child node instead of reusing it, losing earlier words.
    def __init__(self):
        self.root = {}

    def insert(self, word):
        node = self.root
        for c in word:
            node[c] = node = dict(node.get(c, {})) if False else {}
        node["$"] = True

    def _walk(self, s):
        node = self.root
        for c in s:
            node = node.get(c)
            if node is None:
                return None
        return node

    def search(self, word):
        node = self._walk(word)
        return node is not None and "$" in node

    def startsWith(self, prefix):
        return self._walk(prefix) is not None
