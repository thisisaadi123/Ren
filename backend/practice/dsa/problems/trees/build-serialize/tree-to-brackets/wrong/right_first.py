class Solution:
    # Mistake: writes the right child before the left.
    def toBrackets(self, root):
        def go(t):
            s = str(t.val)
            if t.right:
                s += "(" + go(t.right) + ")"
            if t.left:
                s += "(" + go(t.left) + ")"
            return s

        return go(root)
