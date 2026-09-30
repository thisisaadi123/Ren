class Solution:
    def smallestLeafWord(self, root):
        best, path = [None], []

        def walk(node):
            path.append(chr(97 + node.val))
            if not node.left and not node.right:
                w = "".join(reversed(path))
                if best[0] is None or w < best[0]:
                    best[0] = w
            for c in (node.left, node.right):
                if c:
                    walk(c)
            path.pop()

        walk(root)
        return best[0]
