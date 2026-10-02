class Solution:
    def countPaths(self, root, target):
        count = {0: 1}
        total = 0
        stack = [(root, 0, False)]
        while stack:
            node, s, leaving = stack.pop()
            if leaving:
                count[s] -= 1
                continue
            s += node.val
            total += count.get(s - target, 0)
            count[s] = count.get(s, 0) + 1
            stack.append((node, s, True))
            for c in (node.right, node.left):
                if c:
                    stack.append((c, s, False))
        return total
