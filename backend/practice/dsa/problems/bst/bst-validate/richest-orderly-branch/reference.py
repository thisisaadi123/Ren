class Solution:
    def richestOrderlyBranch(self, root):
        order, stack = [], [root]
        while stack:
            node = stack.pop()
            order.append(node)
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        info = {}  # id(node) -> (orderly, low, high, total); children are handled before parents
        best = -float("inf")
        for node in reversed(order):
            v = node.val
            lo, hi, total, ok = v, v, v, True
            if node.left:
                lok, llo, lhi, lsum = info[id(node.left)]
                ok = ok and lok and lhi < v
                lo, total = llo, total + lsum
            if node.right:
                rok, rlo, rhi, rsum = info[id(node.right)]
                ok = ok and rok and rlo > v
                hi, total = rhi, total + rsum
            info[id(node)] = (ok, lo, hi, total)
            if ok and total > best:
                best = total
        return best
