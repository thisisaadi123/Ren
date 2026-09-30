class Solution:
    # Mistake: compares how many nodes each branch has instead of how tall it is.
    def isBalanced(self, root):
        ok = [True]

        def size(node):
            if node is None:
                return 0
            l, r = size(node.left), size(node.right)
            if abs(l - r) > 1:
                ok[0] = False
            return 1 + l + r

        size(root)
        return ok[0]
