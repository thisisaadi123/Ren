class Solution:
    def mostApples(self, root):
        order, stack = [], [root]
        while stack:
            n = stack.pop()
            order.append(n)
            stack += [c for c in (n.left, n.right) if c]
        best = {None: (0, 0)}
        for n in reversed(order):
            lt, ls = best[id(n.left)] if n.left else (0, 0)
            rt, rs = best[id(n.right)] if n.right else (0, 0)
            best[id(n)] = (n.val + ls + rs, max(lt, ls) + max(rt, rs))
        return max(best[id(root)])
