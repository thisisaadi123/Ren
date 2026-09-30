class Solution:
    # Mistake: records the node before its left branch (pre-order, not shelf order).
    def shelfOrder(self, root):
        out, stack = [], [root] if root else []
        while stack:
            node = stack.pop()
            out.append(node.val)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        return out
