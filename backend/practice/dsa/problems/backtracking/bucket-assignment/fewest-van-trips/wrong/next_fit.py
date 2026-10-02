class Solution:
    # Mistake: only ever adds to the most recent trip.
    def fewestTrips(self, boxes, capacity):
        trips, room = 0, 0
        for x in boxes:
            if x > room:
                trips += 1
                room = capacity
            room -= x
        return trips
