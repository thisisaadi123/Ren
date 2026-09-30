class Solution:
    # Mistake: skips every underscore, even doubled ones or one before the first digit.
    def readMeter(self, text):
        n, i = len(text), 0
        while i < n and text[i] == " ":
            i += 1
        sign = 1
        if i < n and text[i] in "+-":
            sign = -1 if text[i] == "-" else 1
            i += 1
        val = 0
        while i < n and (text[i].isdigit() or text[i] == "_"):
            if text[i] != "_":
                val = min(1 << 31, val * 10 + int(text[i]))
            i += 1
        return max(-2**31, min(2**31 - 1, sign * val))
