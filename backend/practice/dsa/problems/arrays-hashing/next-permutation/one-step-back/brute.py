class Solution:
    def stepBack(self, ratings):
        a = ratings
        for i in range(len(a) - 2, -1, -1):
            smaller = [v for v in a[i + 1:] if v < a[i]]
            if smaller:
                d = max(smaller)
                rest = a[i:]
                rest.remove(d)
                return a[:i] + [d] + sorted(rest, reverse=True)
        return sorted(a, reverse=True)
