class Solution:
    # Mistake: takes the remainder of every candidate before comparing them.
    def bestSplitProduct(self, root):
        sums = []

        def total(node):
            if node is None:
                return 0
            s = node.val + total(node.left) + total(node.right)
            sums.append(s)
            return s

        whole = total(root)
        return max(s * (whole - s) % (10**9 + 7) for s in sums)
