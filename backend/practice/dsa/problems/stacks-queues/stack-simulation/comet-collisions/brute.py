class Solution:
    def afterCollisions(self, comets):
        a = list(comets)
        changed = True
        while changed:
            changed = False
            for i in range(len(a) - 1):
                if a[i] > 0 and a[i + 1] < 0:
                    x, y = a[i], -a[i + 1]
                    if x > y:
                        a = a[:i + 1] + a[i + 2:]
                    elif x < y:
                        a = a[:i] + a[i + 1:]
                    else:
                        a = a[:i] + a[i + 2:]
                    changed = True
                    break
        return a
