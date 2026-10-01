class Solution:
    def buildIndex(self, codes):
        def build(lo, hi):
            if lo > hi:
                return None
            mid = (lo + hi) // 2
            return TreeNode(codes[mid], build(lo, mid - 1), build(mid + 1, hi))

        return build(0, len(codes) - 1)
