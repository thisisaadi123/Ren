class Solution:
    def sortByFrequency(self, s):
        count = collections.Counter(s)
        return "".join(ch * count[ch] for ch in sorted(count, key=lambda c: (-count[c], c)))
