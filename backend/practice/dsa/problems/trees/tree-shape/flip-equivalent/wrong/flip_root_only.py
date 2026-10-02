class Solution:
    # Mistake: allows a flip at the root only.
    def flipEquivalent(self, a, b):
        def same(x, y):
            if not x and not y:
                return True
            if not x or not y or x.val != y.val:
                return False
            return same(x.left, y.left) and same(x.right, y.right)

        if not a or not b:
            return a is b
        if a.val != b.val:
            return False
        return (same(a.left, b.left) and same(a.right, b.right)) or (same(a.left, b.right) and same(a.right, b.left))
