class Solution:
    # Mistake: checks each node only against its direct children, not the whole left/right sides.
    def richestOrderlyBranch(self, root):
        best = -float("inf")

        def go(node):
            nonlocal best
            if node is None:
                return True, 0
            lok, ls = go(node.left)
            rok, rs = go(node.right)
            ok = lok and rok
            if node.left and node.left.val >= node.val:
                ok = False
            if node.right and node.right.val <= node.val:
                ok = False
            total = ls + rs + node.val
            if ok:
                best = max(best, total)
            return ok, total

        go(root)
        return best
