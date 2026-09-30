class Solution:
    # Mistake: looks in front instead of behind.
    def countShorterBehind(self, heights):
        return [sum(1 for h in heights[:i] if h < x) for i, x in enumerate(heights)]
