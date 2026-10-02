class Solution:
    # Mistake: compares only the root's two children.
    def isMirror(self, root):
        a, b = root.left, root.right
        if not a or not b:
            return a is b
        return a.val == b.val
