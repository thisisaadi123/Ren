class Solution:
    def isSealed(self, s):
        pair = {")": "(", "]": "[", "}": "{"}
        st = []
        for c in s:
            if c in pair:
                if not st or st[-1] != pair[c]:
                    return False
                st.pop()
            else:
                st.append(c)
        return not st
