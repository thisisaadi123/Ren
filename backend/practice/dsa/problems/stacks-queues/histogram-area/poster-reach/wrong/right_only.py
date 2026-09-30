class Solution:
    # Mistake: only lets the poster spread to the right.
    def posterReach(self, panels):
        n = len(panels)
        right = [n] * n
        st = []
        for i in range(n - 1, -1, -1):
            while st and panels[st[-1]] >= panels[i]:
                st.pop()
            right[i] = st[-1] if st else n
            st.append(i)
        return [right[i] - i for i in range(n)]
