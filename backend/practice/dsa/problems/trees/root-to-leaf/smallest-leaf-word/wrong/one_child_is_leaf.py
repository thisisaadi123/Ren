class Solution:
    # Mistake: treats a missing child as the end of a word, so a one-child node can end a word.
    def smallestLeafWord(self, root):
        best, path = [None], []

        def walk(node):
            if node is None:
                w = "".join(reversed(path))
                if best[0] is None or w < best[0]:
                    best[0] = w
                return
            path.append(chr(97 + node.val))
            walk(node.left)
            walk(node.right)
            path.pop()

        walk(root)
        return best[0]
