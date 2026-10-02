class Solution:
    def deepestAncestor(self, root):
        order, stack = [], [root]
        while stack:
            n = stack.pop()
            order.append(n)
            stack += [c for c in (n.left, n.right) if c]
        info = {}
        for n in reversed(order):
            dl, a = info.get(id(n.left), (0, None))
            dr, b = info.get(id(n.right), (0, None))
            if dl > dr:
                info[id(n)] = (dl + 1, a)
            elif dr > dl:
                info[id(n)] = (dr + 1, b)
            else:
                info[id(n)] = (dl + 1, n.val)
        return info[id(root)][1]
