class Solution:
    def commonOrNone(self, root, p, q):
        order, stack = [], [root]
        while stack:
            n = stack.pop()
            order.append(n)
            stack += [c for c in (n.left, n.right) if c]
        count = {}
        for n in reversed(order):
            c = (n.val == p) + (n.val == q)
            c += count.get(id(n.left), 0) + count.get(id(n.right), 0)
            count[id(n)] = c
            if c == 2:
                return n.val
        return -1
