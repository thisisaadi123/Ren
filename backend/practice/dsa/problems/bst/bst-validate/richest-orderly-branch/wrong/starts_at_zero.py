class Solution:
    # Mistake: starts the best total at 0, as if an empty branch were allowed.
    def richestOrderlyBranch(self, root):
        best = 0

        def go(node):
            nonlocal best
            if node is None:
                return True, float("inf"), -float("inf"), 0
            lok, llo, lhi, ls = go(node.left)
            rok, rlo, rhi, rs = go(node.right)
            ok = lok and rok and lhi < node.val < rlo
            total = ls + rs + node.val
            if ok:
                best = max(best, total)
            return ok, min(llo, node.val), max(rhi, node.val), total

        go(root)
        return best
