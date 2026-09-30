class Solution:
    # Mistake: treats equal values as allowed on either side.
    def richestOrderlyBranch(self, root):
        best = -float("inf")

        def go(node):
            nonlocal best
            if node is None:
                return True, float("inf"), -float("inf"), 0
            lok, llo, lhi, ls = go(node.left)
            rok, rlo, rhi, rs = go(node.right)
            ok = lok and rok and lhi <= node.val <= rlo
            total = ls + rs + node.val
            if ok:
                best = max(best, total)
            return ok, min(llo, node.val), max(rhi, node.val), total

        go(root)
        return best
