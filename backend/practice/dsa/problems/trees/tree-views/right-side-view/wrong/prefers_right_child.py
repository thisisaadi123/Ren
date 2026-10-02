class Solution:
    # Mistake: at each step goes right if possible, else left, from the previous chosen node only.
    def rightView(self, root):
        out = []
        while root:
            out.append(root.val)
            root = root.right or root.left
        return out
