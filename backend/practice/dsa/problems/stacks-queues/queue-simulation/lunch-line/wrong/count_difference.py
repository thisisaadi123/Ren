class Solution:
    # Mistake: assumes only the surplus of one kind goes hungry, ignoring where the stack gets stuck.
    def hungryStudents(self, prefers, trays):
        return abs(prefers.count(0) - trays.count(0))
