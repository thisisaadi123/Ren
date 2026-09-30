class Solution:
    # Mistake: compares with the next code and drops the last one.
    def uniqueSorted(self, codes):
        return [codes[i] for i in range(len(codes) - 1) if codes[i] != codes[i + 1]]
