class Solution:
    # Mistake: finds x and takes the leftmost node of its right side, forgetting ancestors (and absent x).
    def nextTicket(self, root, x):
        node = root
        while node and node.val != x:
            node = node.left if x < node.val else node.right
        if node is None or node.right is None:
            return -1
        node = node.right
        while node.left:
            node = node.left
        return node.val
