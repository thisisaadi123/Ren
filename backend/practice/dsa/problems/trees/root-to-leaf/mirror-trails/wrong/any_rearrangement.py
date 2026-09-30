class Solution:
    # Mistake: counts trails whose digits could be rearranged into a palindrome.
    def mirrorTrails(self, root):
        count, stack = 0, [(root, 0)]
        while stack:
            node, mask = stack.pop()
            mask ^= 1 << node.val
            if not node.left and not node.right:
                count += mask & (mask - 1) == 0
            for c in (node.left, node.right):
                if c:
                    stack.append((c, mask))
        return count
