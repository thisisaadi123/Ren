class Solution:
    # Mistake: returns true for target 0 on an empty map, and treats a missing child as a trail end.
    def hasTrailSum(self, root, target):
        if root is None:
            return target == 0
        return self.hasTrailSum(root.left, target - root.val) or self.hasTrailSum(root.right, target - root.val)
