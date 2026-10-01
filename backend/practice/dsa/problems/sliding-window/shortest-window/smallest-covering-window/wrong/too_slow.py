class Solution:
    # Mistake: from every start, grows a window until it covers t: O(n^2).
    def coverWindow(self, s, t):
        want = {}
        for c in t:
            want[c] = want.get(c, 0) + 1
        best = ""
        for i in range(len(s)):
            have = {}
            left_to_find = len(t)
            for j in range(i, len(s)):
                c = s[j]
                have[c] = have.get(c, 0) + 1
                if have[c] <= want.get(c, 0):
                    left_to_find -= 1
                if left_to_find == 0:
                    if not best or j - i + 1 < len(best):
                        best = s[i:j + 1]
                    break
        return best
