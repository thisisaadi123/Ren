class Solution:
    def countNodes(self, root):
        n, todo = 0, [root] if root else []
        while todo:
            node = todo.pop()
            n += 1
            todo.extend(c for c in (node.left, node.right) if c)
        return n
