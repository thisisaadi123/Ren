class Solution:
    def floorAverages(self, root):
        sums, counts = {}, {}

        def walk(node, d):
            if node:
                sums[d] = sums.get(d, 0) + node.val
                counts[d] = counts.get(d, 0) + 1
                walk(node.left, d + 1)
                walk(node.right, d + 1)

        walk(root, 0)
        return [sums[d] / counts[d] for d in range(len(sums))]
