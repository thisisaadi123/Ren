class Solution:
    # Mistake: when nothing is larger, returns the smallest mirror number instead of "".
    def nextMirror(self, code):
        n = len(code)
        half = list(code[:n // 2])
        i = len(half) - 2
        while i >= 0 and half[i] >= half[i + 1]:
            i -= 1
        if i < 0:
            half.sort()
            k = next((x for x, c in enumerate(half) if c != "0"), 0)
            half[0], half[k] = half[k], half[0]
        else:
            j = len(half) - 1
            while half[j] <= half[i]:
                j -= 1
            half[i], half[j] = half[j], half[i]
            half[i + 1:] = reversed(half[i + 1:])
        left = "".join(half)
        return left + code[n // 2:(n + 1) // 2] + left[::-1]
