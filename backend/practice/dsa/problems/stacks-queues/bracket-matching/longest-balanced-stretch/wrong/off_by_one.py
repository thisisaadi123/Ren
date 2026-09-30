class Solution:
    # Mistake: measures the stretch as i - stack[-1] + 1.
    def longestBalanced(self, s):
        st = [-1]
        best = 0
        for i, c in enumerate(s):
            if c == "(":
                st.append(i)
            else:
                st.pop()
                if not st:
                    st.append(i)
                else:
                    best = max(best, i - st[-1] + 1)
        return best
