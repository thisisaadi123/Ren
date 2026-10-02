class Solution:
    def everySentence(self, text, words):
        n = len(text)
        ws = set(words)
        out = []
        for mask in range(1 << (n - 1)):
            pieces, start = [], 0
            for i in range(1, n):
                if mask >> (i - 1) & 1:
                    pieces.append(text[start:i])
                    start = i
            pieces.append(text[start:])
            if all(p in ws for p in pieces):
                out.append(" ".join(pieces))
        return sorted(out)
