class Solution:
    # Mistake: puts the LARGEST value on top.
    def straighten(self, root):
        dummy = last = TreeNode(0)
        stack, t = [], root
        while stack or t:
            while t:
                stack.append(t)
                t = t.right
            t = stack.pop()
            nxt = t.left
            t.left = None
            last.right = t
            last = t
            t = nxt
        last.right = None
        return dummy.right
