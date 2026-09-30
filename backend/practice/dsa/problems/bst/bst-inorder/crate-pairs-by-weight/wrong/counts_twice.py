class Solution:
    # Mistake: counts every pair from both ends, so each pair is counted twice.
    def countPairs(self, root, target):
        seen, stack = set(), [root]
        while stack:
            node = stack.pop()
            if node:
                seen.add(node.val)
                stack.append(node.left)
                stack.append(node.right)
        return sum(1 for v in seen if target - v in seen and target - v != v)
