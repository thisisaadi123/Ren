class Solution:
    # Mistake: puts a camera on every parent of a leaf and stops there.
    def fewestCameras(self, root):
        if not root.left and not root.right:
            return 1
        count, stack = 0, [root]
        while stack:
            n = stack.pop()
            kids = [c for c in (n.left, n.right) if c]
            if any(not c.left and not c.right for c in kids):
                count += 1
            stack += kids
        return count
