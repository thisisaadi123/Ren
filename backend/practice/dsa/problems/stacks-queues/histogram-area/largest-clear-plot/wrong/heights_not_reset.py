class Solution:
    # Mistake: never resets a column's height on a '0', so it counts every clear cell above, not the unbroken run.
    def largestClearPlot(self, land):
        cols = len(land[0])
        h = [0] * (cols + 1)
        best = 0
        for row in land:
            for c in range(cols):
                if row[c] == "1":
                    h[c] += 1
            st = []
            for i in range(cols + 1):
                while st and h[st[-1]] >= h[i]:
                    top = h[st.pop()]
                    w = i - st[-1] - 1 if st else i
                    best = max(best, top * w)
                st.append(i)
        return best
