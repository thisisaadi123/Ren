class Solution:
    def straighten(self, root):
        dummy = last = TreeNode(0)
        stack, t = [], root
        while stack or t:
            while t:
                stack.append(t)
                t = t.left
            t = stack.pop()
            t.left = None
            last.right = t
            last = t
            t = t.right
        return dummy.right
