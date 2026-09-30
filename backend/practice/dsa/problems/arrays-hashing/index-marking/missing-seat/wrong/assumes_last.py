class Solution:
    # Mistake: returns n + 1 style answer: assumes the free seat is always the last one.
    def missingSeat(self, seats):
        return len(seats)
