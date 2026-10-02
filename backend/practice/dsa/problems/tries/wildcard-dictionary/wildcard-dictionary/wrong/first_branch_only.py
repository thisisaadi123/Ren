class WildcardDictionary:
    # Mistake: at a ".", follows only the first child instead of trying all of them.
    def __init__(self):
        self.root = {}

    def addWord(self, word):
        node = self.root
        for c in word:
            node = node.setdefault(c, {})
        node["$"] = True

    def search(self, pattern):
        node = self.root
        for c in pattern:
            if c == ".":
                kids = [k for k in node if k != "$"]
                if not kids:
                    return False
                node = node[kids[0]]
            elif c in node:
                node = node[c]
            else:
                return False
        return "$" in node
