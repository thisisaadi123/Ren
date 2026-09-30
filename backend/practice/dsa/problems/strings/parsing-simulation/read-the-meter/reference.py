class Solution:
    def readMeter(self, text):
        n, i = len(text), 0
        while i < n and text[i] == " ":
            i += 1
        sign = 1
        if i < n and text[i] in "+-":
            sign = -1 if text[i] == "-" else 1
            i += 1
        cap = 1 << 31
        val, seen = 0, False
        while i < n:
            c = text[i]
            if "0" <= c <= "9":
                val = min(cap, val * 10 + ord(c) - 48)
                seen = True
            elif not (c == "_" and seen and i + 1 < n and "0" <= text[i + 1] <= "9"):
                break
            i += 1
        val *= sign
        return max(-cap, min(cap - 1, val))
