class Solution:
    # Mistake: on a mismatch it only tries deleting the left character.
    def oneSlip(self, s):
        def mirror(i, j):
            while i < j:
                if s[i] != s[j]:
                    return False
                i += 1
                j -= 1
            return True
        i, j = 0, len(s) - 1
        while i < j:
            if s[i] != s[j]:
                return mirror(i + 1, j)
            i += 1
            j -= 1
        return True
