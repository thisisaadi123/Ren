class Solution:
    # Mistake: only tries cutting the two links directly under the root.
    def bestSplitProduct(self, root):
        def total(node):
            return 0 if node is None else node.val + total(node.left) + total(node.right)

        whole = total(root)
        best = max(total(c) * (whole - total(c)) for c in (root.left, root.right) if c)
        return best % (10**9 + 7)
