class Solution:
    def fewestBoats(self, weights, limit):
        a = sorted(weights)
        i, j = 0, len(a) - 1
        boats = 0
        while i <= j:
            if a[i] + a[j] <= limit:
                i += 1
            j -= 1
            boats += 1
        return boats
