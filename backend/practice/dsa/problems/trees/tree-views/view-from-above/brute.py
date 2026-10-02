class Solution:
    def topView(self, root):
        cells = []
        level, depth = [(root, 0)], 0
        while level:
            for pos, (n, c) in enumerate(level):
                cells.append((c, depth, pos, n.val))
            level = [(k, c + d) for n, c in level for k, d in ((n.left, -1), (n.right, 1)) if k]
            depth += 1
        best = {}
        for c, d, pos, v in cells:
            if c not in best or (d, pos) < best[c][:2]:
                best[c] = (d, pos, v)
        return [best[c][2] for c in sorted(best)]
