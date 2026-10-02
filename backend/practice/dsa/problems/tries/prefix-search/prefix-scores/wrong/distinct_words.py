class Solution:
    # Mistake: counts each distinct word once, so repeated words are undercounted.
    def prefixScores(self, words):
        root = {}
        for w in set(words):
            node = root
            for c in w:
                node = node.setdefault(c, {"#": 0})
                node["#"] += 1
        out = []
        for w in words:
            node, total = root, 0
            for c in w:
                node = node[c]
                total += node["#"]
            out.append(total)
        return out
