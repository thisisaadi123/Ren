class Solution:
    # Mistake: compares each code with the next k codes: O(n * k).
    def repeatWithinReach(self, codes, k):
        n = len(codes)
        for i in range(n):
            for j in range(i + 1, min(n, i + k + 1)):
                if codes[i] == codes[j]:
                    return True
        return False
