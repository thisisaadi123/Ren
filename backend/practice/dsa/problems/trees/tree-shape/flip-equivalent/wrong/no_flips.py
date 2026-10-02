class Solution:
    # Mistake: only accepts identical trees.
    def flipEquivalent(self, a, b):
        def same(x, y):
            if not x and not y:
                return True
            if not x or not y or x.val != y.val:
                return False
            return same(x.left, y.left) and same(x.right, y.right)

        return same(a, b)
