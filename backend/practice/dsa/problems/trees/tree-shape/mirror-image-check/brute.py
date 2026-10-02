class Solution:
    def isMirror(self, root):
        def ser(t):
            return None if t is None else (t.val, ser(t.left), ser(t.right))

        def flip(t):
            return None if t is None else (t[0], flip(t[2]), flip(t[1]))

        s = ser(root)
        return s == flip(s)
