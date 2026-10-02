class Solution:
    # Mistake: looks for the branch's in-order values as a run of root's in-order values, ignoring shape.
    def hasBranch(self, root, branch):
        def ino(t):
            out, stack = [], []
            while stack or t:
                while t:
                    stack.append(t)
                    t = t.left
                t = stack.pop()
                out.append(t.val)
                t = t.right
            return out

        a, b = ino(root), ino(branch)
        return any(a[i:i + len(b)] == b for i in range(len(a) - len(b) + 1))
