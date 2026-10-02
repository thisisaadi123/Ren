class Solution:
    # Mistake: attaches every value to the root, filling left then right, ignoring nesting.
    def fromBrackets(self, s):
        import re
        nums = [int(x) for x in re.findall(r"-?\d+", s)]
        root = TreeNode(nums[0])
        level = [root]
        for v in nums[1:]:
            node = TreeNode(v)
            parent = level[(len(level) - 1) // 2]
            if not parent.left:
                parent.left = node
            else:
                parent.right = node
            level.append(node)
        return root
