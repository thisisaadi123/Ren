class Solution:
    def bestSplitProduct(self, root):
        nodes, todo = [], [root]
        while todo:
            node = todo.pop()
            nodes.append(node)
            todo.extend(c for c in (node.left, node.right) if c)

        def subtree(node):
            return 0 if node is None else node.val + subtree(node.left) + subtree(node.right)

        whole = sum(n.val for n in nodes)
        best = 0
        for n in nodes:
            if n is not root:
                s = subtree(n)
                best = max(best, s * (whole - s))
        return best % (10**9 + 7)
