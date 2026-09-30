class Solution:
    # Mistake: treats the band as open, dropping crates that weigh exactly low or high.
    def bandTotal(self, root, low, high):
        total = 0
        stack = [root]
        while stack:
            node = stack.pop()
            if node is None:
                continue
            if node.val <= low:
                stack.append(node.right)
            elif node.val >= high:
                stack.append(node.left)
            else:
                total += node.val
                stack.append(node.left)
                stack.append(node.right)
        return total
