class Solution:
    def countMatches(self, words, patterns):
        root = {}
        for w in words:
            node = root
            for c in w:
                node = node.setdefault(c, {})
            node["$"] = node.get("$", 0) + 1
        out = []
        for p in patterns:
            frontier = [root]
            for c in p:
                nxt = []
                for node in frontier:
                    if c == ".":
                        nxt += [v for k, v in node.items() if k != "$"]
                    elif c in node:
                        nxt.append(node[c])
                frontier = nxt
                if not frontier:
                    break
            out.append(sum(node.get("$", 0) for node in frontier))
        return out
