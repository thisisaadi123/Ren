class Solution:
    # Mistake: hangs the old right child on the right and the old parent on the left.
    def upsideDown(self, root):
        node, prev, prev_right = root, None, None
        while node:
            nxt, right = node.left, node.right
            node.left, node.right = prev, prev_right
            prev, prev_right = node, right
            node = nxt
        return prev
