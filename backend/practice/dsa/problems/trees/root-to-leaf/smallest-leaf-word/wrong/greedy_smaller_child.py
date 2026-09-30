class Solution:
    # Mistake: walks down always taking the child with the smaller letter.
    def smallestLeafWord(self, root):
        path, node = [], root
        while node:
            path.append(chr(97 + node.val))
            kids = [c for c in (node.left, node.right) if c]
            node = min(kids, key=lambda c: c.val) if kids else None
        return "".join(reversed(path))
