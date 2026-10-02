class Solution:
    # Mistake: keeps remainders from finished branches.
    def divisiblePaths(self, root, k):
        count = {0: 1}
        total = 0
        stack = [(root, 0)]
        while stack:
            node, r = stack.pop()
            r = (r + node.val) % k
            total += count.get(r, 0)
            count[r] = count.get(r, 0) + 1
            for c in (node.right, node.left):
                if c:
                    stack.append((c, r))
        return total
