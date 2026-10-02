class Solution:
    def upsideDown(self, root):
        node, prev, prev_right = root, None, None
        while node:
            nxt, right = node.left, node.right
            node.left, node.right = prev_right, prev
            prev, prev_right = node, right
            node = nxt
        return prev
