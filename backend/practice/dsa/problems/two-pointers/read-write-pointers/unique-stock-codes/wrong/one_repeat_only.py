class Solution:
    # Mistake: only removes one extra copy of each code.
    def uniqueSorted(self, codes):
        out = []
        i = 0
        while i < len(codes):
            out.append(codes[i])
            i += 2 if i + 1 < len(codes) and codes[i + 1] == codes[i] else 1
        return out
