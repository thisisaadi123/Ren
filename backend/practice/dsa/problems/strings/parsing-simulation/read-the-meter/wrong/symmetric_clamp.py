class Solution:
    # Mistake: clamps to ±(2³¹ − 1), so the smallest 32-bit value can't be returned.
    def readMeter(self, text):
        n, i = len(text), 0
        while i < n and text[i] == " ":
            i += 1
        sign = 1
        if i < n and text[i] in "+-":
            sign = -1 if text[i] == "-" else 1
            i += 1
        val, seen = 0, False
        while i < n:
            c = text[i]
            if "0" <= c <= "9":
                val = min(1 << 31, val * 10 + ord(c) - 48)
                seen = True
            elif not (c == "_" and seen and i + 1 < n and "0" <= text[i + 1] <= "9"):
                break
            i += 1
        return max(-(2**31 - 1), min(2**31 - 1, sign * val))
