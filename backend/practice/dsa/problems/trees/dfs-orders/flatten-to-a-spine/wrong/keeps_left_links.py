class Solution:
    # Mistake: moves the left branch to the right but never clears the left pointer.
    def flattenToSpine(self, root):
        node = root
        while node:
            if node.left:
                tail = node.left
                while tail.right:
                    tail = tail.right
                tail.right = node.right
                node.right = node.left
            node = node.right
        return root
