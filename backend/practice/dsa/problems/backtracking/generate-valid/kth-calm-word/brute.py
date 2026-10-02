class Solution:
    def kthCalmWord(self, n, k):
        words = [""]
        for _ in range(n):
            words = [w + c for w in words for c in "abc" if not w or w[-1] != c]
        return words[k - 1] if k <= len(words) else ""
