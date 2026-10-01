class Solution:
    def buildIndex(self, codes):
        if not codes:
            return None
        mid = len(codes) // 2
        return TreeNode(codes[mid], self.buildIndex(codes[:mid]), self.buildIndex(codes[mid + 1:]))
