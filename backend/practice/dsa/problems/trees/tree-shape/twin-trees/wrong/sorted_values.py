class Solution:
    # Mistake: compares the multisets of values, ignoring the shape.
    def twins(self, a, b):
        def vals(t, out):
            stack = [t]
            while stack:
                n = stack.pop()
                if n:
                    out.append(n.val)
                    stack += [n.left, n.right]
            return out

        return sorted(vals(a, [])) == sorted(vals(b, []))
