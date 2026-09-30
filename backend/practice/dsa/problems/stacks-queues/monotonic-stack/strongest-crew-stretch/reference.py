class Solution:
    def strongestCrew(self, strength):
        n = len(strength)
        pre = [0] * (n + 1)
        for i, v in enumerate(strength):
            pre[i + 1] = pre[i] + v
        left = [0] * n
        st = []
        for i in range(n):
            while st and strength[st[-1]] >= strength[i]:
                st.pop()
            left[i] = st[-1] + 1 if st else 0
            st.append(i)
        right = [n - 1] * n
        st = []
        for i in range(n - 1, -1, -1):
            while st and strength[st[-1]] >= strength[i]:
                st.pop()
            right[i] = st[-1] - 1 if st else n - 1
            st.append(i)
        return max(strength[i] * (pre[right[i] + 1] - pre[left[i]]) for i in range(n))
