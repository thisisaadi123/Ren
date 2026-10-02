class Solution:
    # Mistake: returns the sentences in the order found.
    def everySentence(self, text, words):
        ws = set(words)

        def go(i):
            if i == len(text):
                return [[]]
            out = []
            for j in range(len(text), i, -1):
                if text[i:j] in ws:
                    out += [[text[i:j]] + rest for rest in go(j)]
            return out

        return [" ".join(s) for s in go(0)]
