class Solution:
    def bestSplitProduct(self, root):
        sums = []

        def total(node):
            if node is None:
                return 0
            s = node.val + total(node.left) + total(node.right)
            sums.append(s)
            return s

        whole = total(root)
        best = max(s * (whole - s) for s in sums)
        return best % (10**9 + 7)
