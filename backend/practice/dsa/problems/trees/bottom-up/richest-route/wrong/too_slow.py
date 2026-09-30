class Solution:
    # Recomputes each node's best downward gain from scratch: O(n^2) on a chain.
    def richestRoute(self, root):
        def down(node):
            # best sum of a path going straight down from node (iterative, no memo)
            best, stack = node.val, [(node, node.val)]
            while stack:
                x, s = stack.pop()
                best = max(best, s)
                for c in (x.left, x.right):
                    if c:
                        stack.append((c, s + c.val))
            return best

        ans, todo = root.val, [root]
        while todo:
            node = todo.pop()
            l = max(0, down(node.left)) if node.left else 0
            r = max(0, down(node.right)) if node.right else 0
            ans = max(ans, node.val + l + r)
            todo.extend(c for c in (node.left, node.right) if c)
        return ans
