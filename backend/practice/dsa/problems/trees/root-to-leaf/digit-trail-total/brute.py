class Solution:
    def digitTrailTotal(self, root):
        words = []

        def walk(node, s):
            s += str(node.val)
            if not node.left and not node.right:
                words.append(s)
            for c in (node.left, node.right):
                if c:
                    walk(c, s)

        walk(root, "")
        return sum(int(w) for w in words) % (10**9 + 7)
