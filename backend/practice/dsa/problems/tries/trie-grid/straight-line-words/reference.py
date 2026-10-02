class Solution:
    def straightWords(self, board, words):
        root = {}
        for w in words:
            node = root
            for c in w:
                node = node.setdefault(c, {})
            node["$"] = w
        m, n = len(board), len(board[0])
        found = set()
        dirs = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1) if a or b]
        for r in range(m):
            for c in range(n):
                if board[r][c] not in root:
                    continue
                for dr, dc in dirs:
                    node, rr, cc = root, r, c
                    while 0 <= rr < m and 0 <= cc < n and board[rr][cc] in node:
                        node = node[board[rr][cc]]
                        if "$" in node:
                            found.add(node["$"])
                        rr += dr
                        cc += dc
        return sorted(found)
