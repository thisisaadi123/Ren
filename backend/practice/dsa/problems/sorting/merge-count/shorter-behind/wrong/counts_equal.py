class Solution:
    # Mistake: counts people of equal height too.
    def countShorterBehind(self, heights):
        return [sum(1 for h in heights[i + 1:] if h <= x) for i, x in enumerate(heights)]
