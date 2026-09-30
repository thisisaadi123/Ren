class Solution:
    def cleanupOrder(self, root):
        out, stack = [], [root] if root else []
        while stack:
            node = stack.pop()
            out.append(node.val)
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        return out[::-1]
