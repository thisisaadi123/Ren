class WildcardDictionary:
    def __init__(self):
        self.root = {}

    def addWord(self, word):
        node = self.root
        for c in word:
            node = node.setdefault(c, {})
        node["$"] = True

    def search(self, pattern):
        frontier = [self.root]
        for c in pattern:
            nxt = []
            for node in frontier:
                if c == ".":
                    nxt += [child for k, child in node.items() if k != "$"]
                elif c in node:
                    nxt.append(node[c])
            frontier = nxt
            if not frontier:
                return False
        return any("$" in node for node in frontier)
