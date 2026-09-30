class Solution:
    # Mistake: takes the biggest single stack layer, but a pool is often several layers together.
    def largestPool(self, walls):
        best = 0
        st = []
        for i, h in enumerate(walls):
            while st and walls[st[-1]] < h:
                mid = st.pop()
                if not st:
                    break
                left = st[-1]
                best = max(best, (min(walls[left], h) - walls[mid]) * (i - left - 1))
            st.append(i)
        return best
