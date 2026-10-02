class Solution:
    def twins(self, a, b):
        def ser(t):
            return None if t is None else (t.val, ser(t.left), ser(t.right))

        return ser(a) == ser(b)
