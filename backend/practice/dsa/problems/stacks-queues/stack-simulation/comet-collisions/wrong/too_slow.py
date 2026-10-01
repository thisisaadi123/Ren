class Solution:
    # Mistake: removes comets from the middle of a list and restarts the scan: O(n^2).
    def afterCollisions(self, comets):
        a = list(comets)
        i = 0
        while i < len(a) - 1:
            if a[i] > 0 and a[i + 1] < 0:
                x, y = a[i], -a[i + 1]
                if x > y:
                    del a[i + 1]
                elif x < y:
                    del a[i]
                else:
                    del a[i:i + 2]
                i = 0
            else:
                i += 1
        return a
