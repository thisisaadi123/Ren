class Solution:
    def toBrackets(self, root):
        def go(t):
            if not t:
                return ""
            s = str(t.val)
            if t.left or t.right:
                s += "(" + go(t.left) + ")"
            if t.right:
                s += "(" + go(t.right) + ")"
            return s

        return go(root)
