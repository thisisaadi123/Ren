class Solution:
    def wordHunt(self, board, words):
        root = {}
        for w in set(words):
            node = root
            for c in w:
                node = node.setdefault(c, {})
            node["$"] = w
        m, n = len(board), len(board[0])
        grid = [list(row) for row in board]
        found = []

        def dfs(r, c, parent):
            ch = grid[r][c]
            node = parent[ch]
            if "$" in node:
                found.append(node.pop("$"))
            grid[r][c] = "#"
            for rr, cc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= rr < m and 0 <= cc < n and grid[rr][cc] in node:
                    dfs(rr, cc, node)
            grid[r][c] = ch
            if not node:
                parent.pop(ch)

        for r in range(m):
            for c in range(n):
                if grid[r][c] in root:
                    dfs(r, c, root)
        return sorted(found)
