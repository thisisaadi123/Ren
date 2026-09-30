class Solution:
    def fixSwappedKeys(self, root):
        first = second = prev = None
        stack, node = [], root
        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            if prev and prev.val > node.val:
                if first is None:
                    first = prev
                second = node
            prev = node
            node = node.right
        first.val, second.val = second.val, first.val
        return root
