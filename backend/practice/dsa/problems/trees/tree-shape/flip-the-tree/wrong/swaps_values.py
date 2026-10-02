class Solution:
    # Mistake: swaps the children's VALUES instead of the subtrees.
    def flip(self, root):
        stack = [root]
        while stack:
            node = stack.pop()
            if node and node.left and node.right:
                node.left.val, node.right.val = node.right.val, node.left.val
            if node:
                stack += [node.left, node.right]
        return root
