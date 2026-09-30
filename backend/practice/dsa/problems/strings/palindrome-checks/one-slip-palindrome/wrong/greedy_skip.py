class Solution:
    # Mistake: on a mismatch it guesses which side to skip by peeking one letter ahead, then commits.
    def oneSlip(self, s):
        i, j, used = 0, len(s) - 1, False
        while i < j:
            if s[i] == s[j]:
                i += 1
                j -= 1
            elif used:
                return False
            else:
                used = True
                if s[i + 1] == s[j]:
                    i += 1
                else:
                    j -= 1
        return True
