class Solution:
    def stripStray(self, s):
        drop = set()
        st = []
        for i, c in enumerate(s):
            if c == "(":
                st.append(i)
            elif c == ")":
                if st:
                    st.pop()
                else:
                    drop.add(i)
        drop.update(st)
        return "".join(c for i, c in enumerate(s) if i not in drop)
