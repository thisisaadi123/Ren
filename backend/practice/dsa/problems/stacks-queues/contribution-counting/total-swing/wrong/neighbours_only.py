class Solution:
    # Mistake: adds up the swings of neighbouring pairs only.
    def totalSwing(self, readings):
        return sum(abs(readings[i + 1] - readings[i]) for i in range(len(readings) - 1))
