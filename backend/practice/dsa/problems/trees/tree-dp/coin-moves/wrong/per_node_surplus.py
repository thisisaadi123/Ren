class Solution:
    # Mistake: adds up how far each node is from one coin, ignoring how far the coins travel.
    def coinMoves(self, root):
        total, stack = 0, [root]
        while stack:
            n = stack.pop()
            if n:
                total += abs(n.val - 1)
                stack += [n.left, n.right]
        return total // 2
