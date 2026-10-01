class Solution:
    def mostVowels(self, s, k):
        vowel = [c in "aeiou" for c in s]
        count = sum(vowel[:k])
        best = count
        for i in range(k, len(s)):
            count += vowel[i] - vowel[i - k]
            best = max(best, count)
        return best
