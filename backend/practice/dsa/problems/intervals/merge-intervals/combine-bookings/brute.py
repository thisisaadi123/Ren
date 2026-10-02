class Solution:
    def combine(self, bookings):
        items = [list(b) for b in bookings]
        changed = True
        while changed:
            changed = False
            for i in range(len(items)):
                for j in range(i + 1, len(items)):
                    a, b = items[i], items[j]
                    if a[0] <= b[1] and b[0] <= a[1]:
                        items[i] = [min(a[0], b[0]), max(a[1], b[1])]
                        items.pop(j)
                        changed = True
                        break
                if changed:
                    break
        return sorted(items)
