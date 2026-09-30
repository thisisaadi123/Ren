class Solution:
    # Mistake: correct, but finds each next key by searching down from the root: O(height) per step.
    def guideSteps(self, root, ops):
        last = None
        out = []
        for op in ops:
            best = None
            node = root
            while node:
                if last is None or node.val > last:
                    best = node
                    node = node.left
                else:
                    node = node.right
            if op == "hasNext":
                out.append(1 if best else 0)
            else:
                out.append(best.val)
                last = best.val
        return out
