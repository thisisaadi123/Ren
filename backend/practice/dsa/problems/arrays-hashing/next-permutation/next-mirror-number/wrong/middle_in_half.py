class Solution:
    # Mistake: lets the middle digit of an odd-length code move with the left half, which changes the digits.
    def nextMirror(self, code):
        n = len(code)
        half = list(code[:(n + 1) // 2])
        i = len(half) - 2
        while i >= 0 and half[i] >= half[i + 1]:
            i -= 1
        if i < 0:
            return ""
        j = len(half) - 1
        while half[j] <= half[i]:
            j -= 1
        half[i], half[j] = half[j], half[i]
        half[i + 1:] = reversed(half[i + 1:])
        left = "".join(half)
        return left + left[:n // 2][::-1]
