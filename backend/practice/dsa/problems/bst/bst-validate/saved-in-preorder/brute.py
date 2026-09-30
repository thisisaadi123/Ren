class Solution:
    def couldBePreorder(self, keys):
        # Insert the keys in order into a search tree; its preorder must give the keys back.
        left, right = {}, {}
        root = keys[0]
        for k in keys[1:]:
            cur = root
            while True:
                side = left if k < cur else right
                if cur in side:
                    cur = side[cur]
                else:
                    side[cur] = k
                    break
        out = []

        def pre(x):
            if x is None:
                return
            out.append(x)
            pre(left.get(x))
            pre(right.get(x))

        pre(root)
        return out == keys
