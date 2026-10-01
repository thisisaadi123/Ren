class Solution:
    # Mistake: allows three flavours in the cone.
    def mostScoops(self, flavours):
        count = {}
        left = best = 0
        for i, f in enumerate(flavours):
            count[f] = count.get(f, 0) + 1
            while len(count) > 3:
                g = flavours[left]
                count[g] -= 1
                if count[g] == 0:
                    del count[g]
                left += 1
            best = max(best, i - left + 1)
        return best
