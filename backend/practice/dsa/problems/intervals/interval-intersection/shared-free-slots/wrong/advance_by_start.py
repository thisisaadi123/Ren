class Solution:
    # Mistake: moves past the slot that STARTS first, which may still overlap later slots.
    def sharedSlots(self, a, b):
        i = j = 0
        out = []
        while i < len(a) and j < len(b):
            s = max(a[i][0], b[j][0])
            e = min(a[i][1], b[j][1])
            if s <= e:
                out.append([s, e])
            if a[i][0] < b[j][0]:
                i += 1
            else:
                j += 1
        return out
