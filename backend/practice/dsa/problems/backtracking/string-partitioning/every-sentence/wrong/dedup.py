class Solution:
    # Mistake: keeps only one sentence per number of words.
    def everySentence(self, text, words):
        ws = set(words)

        def go(i):
            if i == len(text):
                return [[]]
            out = []
            for j in range(i + 1, len(text) + 1):
                if text[i:j] in ws:
                    out += [[text[i:j]] + rest for rest in go(j)]
            return out

        by_len = {}
        for s in go(0):
            by_len.setdefault(len(s), " ".join(s))
        return sorted(by_len.values())
