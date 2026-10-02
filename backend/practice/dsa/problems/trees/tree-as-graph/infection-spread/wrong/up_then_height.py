class Solution:
    # Mistake: adds the start's depth to the whole tree's height, as if the virus always went through the root.
    def minutesToSpread(self, root, start):
        level, d, h, found = [root], 0, -1, 0
        while level:
            h += 1
            if any(n.val == start for n in level):
                found = h
            level = [c for n in level for c in (n.left, n.right) if c]
        return found + h if start != root.val else h
