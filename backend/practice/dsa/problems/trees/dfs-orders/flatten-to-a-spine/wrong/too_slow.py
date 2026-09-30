class Solution:
    # Flattens the left branch, then walks from its head to its tail every time: O(n^2) on a left chain.
    def flattenToSpine(self, root):
        def flat(node):
            if node is None:
                return None
            left, right = flat(node.left), flat(node.right)
            node.left = None
            if left:
                node.right = left
                tail = left
                while tail.right:
                    tail = tail.right
                tail.right = right
            else:
                node.right = right
            return node

        return flat(root)
