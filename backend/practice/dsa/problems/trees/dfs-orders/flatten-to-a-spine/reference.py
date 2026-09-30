class Solution:
    def flattenToSpine(self, root):
        node = root
        while node:
            if node.left:
                tail = node.left
                while tail.right:
                    tail = tail.right
                tail.right = node.right
                node.right = node.left
                node.left = None
            node = node.right
        return root
