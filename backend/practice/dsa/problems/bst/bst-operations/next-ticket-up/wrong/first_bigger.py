class Solution:
    # Mistake: stops at the first bigger ticket on the path instead of looking left for a smaller one.
    def nextTicket(self, root, x):
        node = root
        while node:
            if node.val > x:
                return node.val
            node = node.right
        return -1
