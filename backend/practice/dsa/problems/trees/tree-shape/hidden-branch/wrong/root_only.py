class Solution:
    # Mistake: compares the branch with the whole tree only.
    def hasBranch(self, root, branch):
        def same(a, b):
            if not a and not b:
                return True
            if not a or not b or a.val != b.val:
                return False
            return same(a.left, b.left) and same(a.right, b.right)

        return same(root, branch)
