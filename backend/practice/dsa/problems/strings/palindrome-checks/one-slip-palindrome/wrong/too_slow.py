class Solution:
    # Tries deleting every position and rechecks the whole string each time: O(n²).
    def oneSlip(self, s):
        def mirror(t):
            i, j = 0, len(t) - 1
            while i < j:
                if t[i] != t[j]:
                    return False
                i += 1
                j -= 1
            return True
        if mirror(s):
            return True
        for k in range(len(s)):
            if mirror(s[:k] + s[k + 1:]):
                return True
        return False
