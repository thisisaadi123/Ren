class Solution:
    # Mistake: starts the right half one past where it should, skipping a code.
    def buildIndex(self, codes):
        def build(lo, hi):
            if lo > hi:
                return None
            mid = (lo + hi) // 2
            return TreeNode(codes[mid], build(lo, mid - 1), build(mid + 2, hi))

        return build(0, len(codes) - 1)
