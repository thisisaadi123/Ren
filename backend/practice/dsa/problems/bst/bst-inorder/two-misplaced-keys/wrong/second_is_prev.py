class Solution:
    # Mistake: at the second drop it takes the larger value (prev) instead of the smaller one.
    def fixSwappedKeys(self, root):
        first = second = prev = None
        drops = 0
        stack, node = [], root
        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            if prev and prev.val > node.val:
                drops += 1
                if drops == 1:
                    first, second = prev, node
                else:
                    second = prev
            prev = node
            node = node.right
        first.val, second.val = second.val, first.val
        return root
