class Solution:
    # Mistake: never adds the extra camera when the root is left unwatched.
    def fewestCameras(self, root):
        order, stack = [], [root]
        while stack:
            n = stack.pop()
            order.append(n)
            stack += [c for c in (n.left, n.right) if c]
        state, cams = {}, 0
        for n in reversed(order):
            kids = [state[id(c)] for c in (n.left, n.right) if c]
            if 0 in kids:
                state[id(n)] = 1
                cams += 1
            elif 1 in kids:
                state[id(n)] = 2
            else:
                state[id(n)] = 0
        return max(1, cams)
