class Solution:
    def largestClearPlot(self, land):
        cols = len(land[0])
        h = [0] * (cols + 1)
        best = 0
        for row in land:
            for c in range(cols):
                h[c] = h[c] + 1 if row[c] == "1" else 0
            st = []
            for i in range(cols + 1):
                while st and h[st[-1]] >= h[i]:
                    top = h[st.pop()]
                    w = i - st[-1] - 1 if st else i
                    if top * w > best:
                        best = top * w
                st.append(i)
        return best
