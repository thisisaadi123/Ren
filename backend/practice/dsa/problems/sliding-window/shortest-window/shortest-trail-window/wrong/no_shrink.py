class Solution:
    # Mistake: from each start letter, matches forward greedily but never tightens the window from the left.
    def trailWindow(self, s, t):
        best = ""
        i = 0
        while i < len(s):
            if s[i] == t[0]:
                j, k = i, 0
                while j < len(s) and k < len(t):
                    if s[j] == t[k]:
                        k += 1
                    j += 1
                if k == len(t):
                    if not best or j - i < len(best):
                        best = s[i:j]
                    i = j
                    continue
                break
            i += 1
        return best
