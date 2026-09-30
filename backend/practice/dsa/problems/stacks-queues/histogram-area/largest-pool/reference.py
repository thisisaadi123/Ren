class Solution:
    def largestPool(self, walls):
        n = len(walls)
        water = [0] * n
        st = []
        for i, h in enumerate(walls):
            while st and walls[st[-1]] < h:
                mid = st.pop()
                if not st:
                    break
                left = st[-1]
                level = min(walls[left], h)
                for_layer = level - walls[mid]
                # every column strictly between left and i rises by this layer
                water[left + 1] += for_layer
                water[i] -= for_layer
            st.append(i)
        best = run = level = 0
        for i in range(n):
            level += water[i]
            if level > 0:
                run += level
                best = max(best, run)
            else:
                run = 0
        return best
