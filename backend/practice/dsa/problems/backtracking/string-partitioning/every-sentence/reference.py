class Solution:
    def everySentence(self, text, words):
        ws = set(words)
        memo = {}

        def go(i):
            if i == len(text):
                return [[]]
            if i not in memo:
                out = []
                for j in range(i + 1, len(text) + 1):
                    if text[i:j] in ws:
                        out += [[text[i:j]] + rest for rest in go(j)]
                memo[i] = out
            return memo[i]

        return sorted(" ".join(s) for s in go(0))
