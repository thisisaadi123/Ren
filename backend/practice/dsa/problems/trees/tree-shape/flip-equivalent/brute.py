class Solution:
    def flipEquivalent(self, a, b):
        def canon(t):
            if t is None:
                return None
            kids = sorted((canon(t.left), canon(t.right)), key=repr)
            return (t.val, kids[0], kids[1])

        return canon(a) == canon(b)
