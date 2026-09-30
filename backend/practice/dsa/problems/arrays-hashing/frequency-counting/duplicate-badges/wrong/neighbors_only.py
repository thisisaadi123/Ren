class Solution:
    # Mistake: only compares neighbours, without sorting first.
    def hasDuplicate(self, badges):
        return any(badges[i] == badges[i + 1] for i in range(len(badges) - 1))
