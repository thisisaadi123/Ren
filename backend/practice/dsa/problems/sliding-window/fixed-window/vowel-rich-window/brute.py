class Solution:
    def mostVowels(self, s, k):
        return max(sum(c in "aeiou" for c in s[i:i + k]) for i in range(len(s) - k + 1))
