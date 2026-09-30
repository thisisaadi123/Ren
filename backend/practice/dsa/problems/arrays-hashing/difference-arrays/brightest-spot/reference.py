class Solution:
    def brightestSpot(self, lamps):
        events = collections.Counter()
        for pos, reach in lamps:
            events[pos - reach] += 1
            events[pos + reach + 1] -= 1
        best, best_at, running = -1, None, 0
        for x in sorted(events):
            running += events[x]
            if running > best:
                best, best_at = running, x
        return best_at
