class Solution:
    # Mistake: deletes matched "()" pairs one sweep at a time: O(n²) on deep nesting.
    def minInsertions(self, s):
        st = list(s)
        changed = True
        while changed:
            changed, out, i = False, [], 0
            while i < len(st):
                if i + 1 < len(st) and st[i] == "(" and st[i + 1] == ")":
                    i += 2
                    changed = True
                else:
                    out.append(st[i]); i += 1
            st = out
        return len(st)
