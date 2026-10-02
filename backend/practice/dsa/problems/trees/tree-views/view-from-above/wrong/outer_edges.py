class Solution:
    # Mistake: reads only the left spine (reversed), the root and the right spine.
    def topView(self, root):
        left, node = [], root.left
        while node:
            left.append(node.val)
            node = node.left
        right, node = [], root.right
        while node:
            right.append(node.val)
            node = node.right
        return left[::-1] + [root.val] + right
