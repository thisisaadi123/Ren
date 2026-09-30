class Solution:
    # Correct but O(n^2).
    def hasDuplicate(self, badges):
        n = len(badges)
        for i in range(n):
            for j in range(i + 1, n):
                if badges[i] == badges[j]:
                    return True
        return False
