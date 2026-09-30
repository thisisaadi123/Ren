class Solution:
    # Mistake: measures the width as right − left, counting one wall panel.
    def posterReach(self, panels):
        n = len(panels)
        left, right = [-1] * n, [n] * n
        st = []
        for i in range(n):
            while st and panels[st[-1]] >= panels[i]:
                st.pop()
            left[i] = st[-1] if st else -1
            st.append(i)
        st = []
        for i in range(n - 1, -1, -1):
            while st and panels[st[-1]] >= panels[i]:
                st.pop()
            right[i] = st[-1] if st else n
            st.append(i)
        return [min(n, right[i] - left[i]) for i in range(n)]
