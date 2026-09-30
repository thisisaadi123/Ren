class Solution:
    # Mistake: ties keep the order of first appearance instead of character order.
    def sortByFrequency(self, s):
        return "".join(ch * n for ch, n in collections.Counter(s).most_common())
