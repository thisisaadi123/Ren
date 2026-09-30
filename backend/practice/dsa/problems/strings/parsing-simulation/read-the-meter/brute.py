import re
class Solution:
    def readMeter(self, text):
        m = re.match(r" *([+-]?)([0-9]+(?:_[0-9]+)*)", text)
        if not m:
            return 0
        v = int(m.group(2).replace("_", ""))
        if m.group(1) == "-":
            v = -v
        return max(-2**31, min(2**31 - 1, v))
