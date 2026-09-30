class Solution:
    # Mistake: adds the floor up in a 32-bit integer, which overflows on big figures.
    def floorAverages(self, root):
        out, level = [], [root]
        while level:
            s = 0
            for n in level:
                s = (s + n.val + 2**31) % 2**32 - 2**31
            out.append(s / len(level))
            level = [c for n in level for c in (n.left, n.right) if c]
        return out
