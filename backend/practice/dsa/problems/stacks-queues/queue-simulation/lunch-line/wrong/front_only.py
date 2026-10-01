class Solution:
    # Mistake: stops as soon as the FRONT student doesn't want the tray, without anyone going round.
    def hungryStudents(self, prefers, trays):
        i = 0
        while i < len(trays) and prefers[i] == trays[i]:
            i += 1
        return len(trays) - i
