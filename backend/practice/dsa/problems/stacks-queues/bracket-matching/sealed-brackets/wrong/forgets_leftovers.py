class Solution:
    # Mistake: never checks that the stack is empty at the end.
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
        return True
