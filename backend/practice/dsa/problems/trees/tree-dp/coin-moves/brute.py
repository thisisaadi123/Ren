class Solution:
    def coinMoves(self, root):
        nodes = []

        def collect(t):
            if t:
                nodes.append(t)
                collect(t.left)
                collect(t.right)

        collect(root)

        def totals(t):
            if not t:
                return 0, 0
            c1, n1 = totals(t.left)
            c2, n2 = totals(t.right)
            return t.val + c1 + c2, 1 + n1 + n2

        moves = 0
        for t in nodes:
            for c in (t.left, t.right):
                if c:
                    coins, count = totals(c)
                    moves += abs(coins - count)
        return moves
