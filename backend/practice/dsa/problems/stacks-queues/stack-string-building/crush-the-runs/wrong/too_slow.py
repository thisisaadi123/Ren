class Solution:
    # Mistake: rescans the whole string after every crush: O(n^2 / k).
    def crushRuns(self, s, k):
        changed = True
        while changed:
            changed = False
            run = 1
            for i in range(1, len(s) + 1):
                if i < len(s) and s[i] == s[i - 1]:
                    run += 1
                    if run == k:
                        s = s[:i - k + 1] + s[i + 1:]
                        changed = True
                        break
                else:
                    run = 1
        return s
