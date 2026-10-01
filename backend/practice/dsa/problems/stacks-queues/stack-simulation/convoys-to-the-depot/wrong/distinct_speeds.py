class Solution:
    # Mistake: assumes trucks with the same speed form one convoy.
    def convoys(self, depot, position, speed):
        return len(set(speed))
