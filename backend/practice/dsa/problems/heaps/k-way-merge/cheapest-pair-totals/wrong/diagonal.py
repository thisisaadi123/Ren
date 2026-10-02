class Solution:
    # Mistake: walks the two lists like a merge, only ever pairing neighbours.
    def cheapestPairs(self, a, b, k):
        i = j = 0
        out = [a[0] + b[0]]
        while len(out) < k:
            if j + 1 < len(b) and (i + 1 >= len(a) or a[i] + b[j + 1] <= a[i + 1] + b[j]):
                j += 1
            else:
                i += 1
            out.append(a[i] + b[j])
        return out
