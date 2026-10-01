class Solution:
    # Mistake: treats y as a vowel.
    def mostVowels(self, s, k):
        vowel = [c in "aeiouy" for c in s]
        count = sum(vowel[:k])
        best = count
        for i in range(k, len(s)):
            count += vowel[i] - vowel[i - k]
            best = max(best, count)
        return best
