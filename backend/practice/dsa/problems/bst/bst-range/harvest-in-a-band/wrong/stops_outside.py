class Solution:
    # Mistake: stops at the first node outside the band, missing keys further down.
    def bandTotal(self, root, low, high):
        total = 0
        stack = [root]
        while stack:
            node = stack.pop()
            if node is None or not low <= node.val <= high:
                continue
            total += node.val
            stack.append(node.left)
            stack.append(node.right)
        return total
