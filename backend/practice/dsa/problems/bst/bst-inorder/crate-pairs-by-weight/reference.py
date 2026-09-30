class Solution:
    def countPairs(self, root, target):
        lo_stack, hi_stack = [], []

        def push_left(node):
            while node:
                lo_stack.append(node)
                node = node.left

        def push_right(node):
            while node:
                hi_stack.append(node)
                node = node.right

        push_left(root)
        push_right(root)
        count = 0
        while lo_stack and hi_stack:
            a, b = lo_stack[-1], hi_stack[-1]
            if a.val >= b.val:
                break
            s = a.val + b.val
            if s <= target:
                lo_stack.pop()
                push_left(a.right)
            if s >= target:
                hi_stack.pop()
                push_right(b.left)
            if s == target:
                count += 1
        return count
