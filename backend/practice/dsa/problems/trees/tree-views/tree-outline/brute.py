class Solution:
    def outline(self, root):
        def leaf(n):
            return not n.left and not n.right

        if leaf(root):
            return [root.val]

        def edge(n, first):
            path = []
            while n:
                path.append(n)
                n = (n.left or n.right) if first == "L" else (n.right or n.left)
            return [x for x in path if not leaf(x)]

        leaves = []

        def walk(n):
            if n:
                if leaf(n):
                    leaves.append(n)
                walk(n.left)
                walk(n.right)

        walk(root.left)
        walk(root.right)
        left = edge(root.left, "L")
        right = edge(root.right, "R")
        return [root.val] + [x.val for x in left] + [x.val for x in leaves] + [x.val for x in reversed(right)]
