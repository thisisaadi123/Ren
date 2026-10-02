class Solution:
    def threadedInorder(self, root):
        out = []

        def go(t):
            if t:
                go(t.left)
                out.append(t.val)
                go(t.right)

        go(root)
        return out
