class Solution:
    # Recomputes the subtree total from scratch for every possible cut: O(n^2) on a chain.
    def bestSplitProduct(self, root):
        def subtree(node):
            s, todo = 0, [node]
            while todo:
                x = todo.pop()
                s += x.val
                todo.extend(c for c in (x.left, x.right) if c)
            return s

        whole = subtree(root)
        best, todo = 0, [root]
        while todo:
            node = todo.pop()
            for c in (node.left, node.right):
                if c:
                    s = subtree(c)
                    best = max(best, s * (whole - s))
                    todo.append(c)
        return best % (10**9 + 7)
