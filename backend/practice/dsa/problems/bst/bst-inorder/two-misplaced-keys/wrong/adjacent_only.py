class Solution:
    # Mistake: assumes the swapped keys are neighbours in sorted order and fixes only the first drop.
    def fixSwappedKeys(self, root):
        prev = None
        stack, node = [], root
        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            if prev and prev.val > node.val:
                prev.val, node.val = node.val, prev.val
                return root
            prev = node
            node = node.right
        return root
