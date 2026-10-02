class Solution:
    def mergeWithin(self, shifts, gap):
        items = [list(x) for x in shifts]
        changed = True
        while changed:
            changed = False
            for i in range(len(items)):
                for j in range(len(items)):
                    if i != j:
                        a, b = items[i], items[j]
                        if b[0] - a[1] <= gap and a[0] - b[1] <= gap:
                            items[i] = [min(a[0], b[0]), max(a[1], b[1])]
                            items.pop(j)
                            changed = True
                            break
                if changed:
                    break
        return sorted(items)
