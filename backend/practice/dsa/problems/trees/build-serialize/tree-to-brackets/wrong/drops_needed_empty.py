class Solution:
    # Mistake: leaves out the "()" for a missing left child even when a right child follows.
    def toBrackets(self, root):
        def go(t):
            s = str(t.val)
            if t.left:
                s += "(" + go(t.left) + ")"
            if t.right:
                s += "(" + go(t.right) + ")"
            return s

        return go(root)
