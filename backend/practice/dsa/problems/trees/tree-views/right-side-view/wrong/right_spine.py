class Solution:
    # Mistake: follows right children only, missing levels that are deeper on the left.
    def rightView(self, root):
        out = []
        while root:
            out.append(root.val)
            root = root.right
        return out
