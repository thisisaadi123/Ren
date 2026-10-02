class Solution:
    # Mistake: divides the total weight by the capacity.
    def fewestTrips(self, boxes, capacity):
        return -(-sum(boxes) // capacity)
