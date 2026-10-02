class Solution:
    # Mistake: counts only coins that move up towards the root, not those that move down.
    def coinMoves(self, root):
        order, stack = [], [root]
        while stack:
            node = stack.pop()
            order.append(node)
            stack += [c for c in (node.left, node.right) if c]
        extra = {}
        moves = 0
        for node in reversed(order):
            el = extra[id(node.left)] if node.left else 0
            er = extra[id(node.right)] if node.right else 0
            moves += max(0, el) + max(0, er)
            extra[id(node)] = node.val - 1 + el + er
        return moves
