class Solution:
    # Mistake: first-fit decreasing, a good heuristic but not always optimal.
    def fewestTrips(self, boxes, capacity):
        room = []
        for x in sorted(boxes, reverse=True):
            for t in range(len(room)):
                if room[t] >= x:
                    room[t] -= x
                    break
            else:
                room.append(capacity - x)
        return len(room)
