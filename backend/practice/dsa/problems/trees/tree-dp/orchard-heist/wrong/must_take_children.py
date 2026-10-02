class Solution:
    # Mistake: when a tree is skipped, forces both children to be picked.
    def mostApples(self, root):
        order, stack = [], [root]
        while stack:
            n = stack.pop()
            order.append(n)
            stack += [c for c in (n.left, n.right) if c]
        best = {}
        for n in reversed(order):
            lt, ls = best[id(n.left)] if n.left else (0, 0)
            rt, rs = best[id(n.right)] if n.right else (0, 0)
            best[id(n)] = (n.val + ls + rs, lt + rt)
        return max(best[id(root)])
