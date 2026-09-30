class Solution:
    def countPairs(self, root, target):
        vals, stack = [], [root]
        while stack:
            node = stack.pop()
            if node:
                vals.append(node.val)
                stack.append(node.left)
                stack.append(node.right)
        n = len(vals)
        return sum(1 for i in range(n) for j in range(i + 1, n) if vals[i] + vals[j] == target)
