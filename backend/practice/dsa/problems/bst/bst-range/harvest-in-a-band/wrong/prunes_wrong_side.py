class Solution:
    # Mistake: below the band it keeps searching left instead of right.
    def bandTotal(self, root, low, high):
        total = 0
        stack = [root]
        while stack:
            node = stack.pop()
            if node is None:
                continue
            if node.val < low:
                stack.append(node.left)
            elif node.val > high:
                stack.append(node.right)
            else:
                total += node.val
                stack.append(node.left)
                stack.append(node.right)
        return total
