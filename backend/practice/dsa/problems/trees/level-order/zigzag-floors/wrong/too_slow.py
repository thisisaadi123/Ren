class Solution:
    # Re-walks the whole tree to collect each floor: O(n * height).
    def zigzagFloors(self, root):
        out, d = [], 0
        while root:
            vals, stack = [], [(root, 0)]
            while stack:
                node, k = stack.pop()
                if k == d:
                    vals.append(node.val)
                    continue
                for ch in (node.right, node.left):
                    if ch:
                        stack.append((ch, k + 1))
            if not vals:
                break
            out.append(vals[::-1] if d % 2 else vals)
            d += 1
        return out
