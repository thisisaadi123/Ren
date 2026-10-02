class Solution:
    # Mistake: writes "()" for every missing child.
    def toBrackets(self, root):
        def go(t):
            if not t:
                return ""
            if not t.left and not t.right:
                return str(t.val)
            return str(t.val) + "(" + go(t.left) + ")(" + go(t.right) + ")"

        return go(root)
