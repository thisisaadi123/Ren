class Solution:
    # Mistake: never removes a prefix when leaving a node, so other branches can use it.
    def countPaths(self, root, target):
        count = {0: 1}
        total = 0
        stack = [(root, 0)]
        while stack:
            node, s = stack.pop()
            s += node.val
            total += count.get(s - target, 0)
            count[s] = count.get(s, 0) + 1
            for c in (node.right, node.left):
                if c:
                    stack.append((c, s))
        return total
