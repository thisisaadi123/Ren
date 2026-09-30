class Solution:
    # Mistake: repeatedly deletes adjacent matching pairs, one sweep at a time: O(n²) on deep nesting.
    def isSealed(self, s):
        match = {"(": ")", "[": "]", "{": "}"}
        st = list(s)
        changed = True
        while changed:
            changed, out, i = False, [], 0
            while i < len(st):
                if i + 1 < len(st) and match.get(st[i]) == st[i + 1]:
                    i += 2
                    changed = True
                else:
                    out.append(st[i]); i += 1
            st = out
        return not st
