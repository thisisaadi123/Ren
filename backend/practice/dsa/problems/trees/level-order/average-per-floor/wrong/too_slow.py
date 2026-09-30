class Solution:
    # Walks the whole tree again for every floor: O(n * height).
    def floorAverages(self, root):
        out, d = [], 0
        while True:
            s = c = 0
            stack = [(root, 0)]
            while stack:
                node, k = stack.pop()
                if k == d:
                    s += node.val
                    c += 1
                    continue
                for ch in (node.left, node.right):
                    if ch:
                        stack.append((ch, k + 1))
            if c == 0:
                return out
            out.append(s / c)
            d += 1
