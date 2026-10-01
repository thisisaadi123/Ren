class Solution:
    # Mistake: recounts every window: O(n * k).
    def mostVowels(self, s, k):
        best = 0
        for i in range(len(s) - k + 1):
            c = 0
            for ch in s[i:i + k]:
                if ch in "aeiou":
                    c += 1
            best = max(best, c)
        return best
