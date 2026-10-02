class Solution:
    def fewestTrips(self, boxes, capacity):
        xs = sorted(boxes, reverse=True)
        best = [len(xs)]
        room = []

        def go(i):
            if len(room) >= best[0]:
                return
            if i == len(xs):
                best[0] = len(room)
                return
            seen = set()
            for t in range(len(room)):
                if room[t] >= xs[i] and room[t] not in seen:
                    seen.add(room[t])
                    room[t] -= xs[i]
                    go(i + 1)
                    room[t] += xs[i]
            room.append(capacity - xs[i])
            go(i + 1)
            room.pop()

        go(0)
        return best[0]
