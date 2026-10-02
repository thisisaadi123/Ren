class Solution:
    def hasBranch(self, root, branch):
        def ser(t):
            return None if t is None else (t.val, ser(t.left), ser(t.right))

        want = ser(branch)

        def walk(t):
            return t is not None and (ser(t) == want or walk(t.left) or walk(t.right))

        return walk(root)
