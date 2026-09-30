class Solution:
    def nextTicket(self, root, x):
        vals, stack = [], [root]
        while stack:
            node = stack.pop()
            if node:
                vals.append(node.val)
                stack.append(node.left)
                stack.append(node.right)
        bigger = [v for v in vals if v > x]
        return min(bigger) if bigger else -1
