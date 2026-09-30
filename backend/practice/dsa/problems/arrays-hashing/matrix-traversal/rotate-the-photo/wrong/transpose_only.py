class Solution:
    # Mistake: only transposes.
    def rotateClockwise(self, photo):
        return [list(c) for c in zip(*photo)]
