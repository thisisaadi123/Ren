class Solution:
    def nextTicket(self, root, x):
        best = -1
        node = root
        while node:
            if node.val > x:
                best = node.val
                node = node.left
            else:
                node = node.right
        return best
