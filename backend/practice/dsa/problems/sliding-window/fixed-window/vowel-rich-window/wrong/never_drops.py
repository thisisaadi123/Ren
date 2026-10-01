class Solution:
    # Mistake: adds vowels as they enter but never removes the ones that leave.
    def mostVowels(self, s, k):
        count = sum(c in "aeiou" for c in s[:k])
        best = count
        for i in range(k, len(s)):
            count += s[i] in "aeiou"
            best = max(best, min(count, k))
        return best
