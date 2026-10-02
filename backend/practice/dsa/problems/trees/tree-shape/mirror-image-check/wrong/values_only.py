class Solution:
    # Mistake: checks that each level's values read the same both ways, ignoring gaps.
    def isMirror(self, root):
        level = [root]
        while level:
            vals = [n.val for n in level]
            if vals != vals[::-1]:
                return False
            level = [c for n in level for c in (n.left, n.right) if c]
        return True
