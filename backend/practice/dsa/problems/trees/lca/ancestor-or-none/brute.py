class Solution:
    def commonOrNone(self, root, p, q):
        def path(t, target):
            if not t:
                return None
            if t.val == target:
                return [t.val]
            for c in (t.left, t.right):
                r = path(c, target)
                if r:
                    return [t.val] + r
            return None

        a, b = path(root, p), path(root, q)
        if not a or not b:
            return -1
        i = 0
        while i < min(len(a), len(b)) and a[i] == b[i]:
            i += 1
        return a[i - 1]
