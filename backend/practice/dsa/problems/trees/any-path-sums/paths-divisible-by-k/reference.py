class Solution:
    def divisiblePaths(self, root, k):
        count = {0: 1}
        total = 0
        stack = [(root, 0, False)]
        while stack:
            node, r, leaving = stack.pop()
            if leaving:
                count[r] -= 1
                continue
            r = (r + node.val) % k
            total += count.get(r, 0)
            count[r] = count.get(r, 0) + 1
            stack.append((node, r, True))
            for c in (node.right, node.left):
                if c:
                    stack.append((c, r, False))
        return total
