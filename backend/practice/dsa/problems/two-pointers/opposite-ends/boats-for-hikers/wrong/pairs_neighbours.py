class Solution:
    # Mistake: pairs neighbours in sorted order.
    def fewestBoats(self, weights, limit):
        a = sorted(weights)
        boats = i = 0
        while i < len(a):
            if i + 1 < len(a) and a[i] + a[i + 1] <= limit:
                i += 2
            else:
                i += 1
            boats += 1
        return boats
