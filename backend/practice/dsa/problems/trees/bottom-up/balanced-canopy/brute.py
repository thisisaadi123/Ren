class Solution:
    def isBalanced(self, root):
        def h(node):
            return 0 if node is None else 1 + max(h(node.left), h(node.right))

        nodes, todo = [], [root] if root else []
        while todo:
            node = todo.pop()
            nodes.append(node)
            todo.extend(c for c in (node.left, node.right) if c)
        return all(abs(h(n.left) - h(n.right)) <= 1 for n in nodes)
