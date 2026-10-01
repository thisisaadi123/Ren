class Solution:
    # Mistake: answers with the number of guests in the first run instead of the best run.
    def fewestSwaps(self, seats):
        t = sum(seats)
        return t - sum(seats[:t])
