class Solution:
    def mostApples(self, root):
        nodes, parent, stack = [], {}, [(root, None)]
        while stack:
            n, p = stack.pop()
            parent[len(nodes)] = p
            me = len(nodes)
            nodes.append(n.val)
            stack += [(c, me) for c in (n.left, n.right) if c]
        k = len(nodes)
        if k <= 14:
            best = 0
            for mask in range(1 << k):
                if any(mask >> i & 1 and parent[i] is not None and mask >> parent[i] & 1 for i in range(k)):
                    continue
                best = max(best, sum(nodes[i] for i in range(k) if mask >> i & 1))
            return best

        def go(t, can):
            if not t:
                return 0
            skip = go(t.left, True) + go(t.right, True)
            return max(skip, t.val + go(t.left, False) + go(t.right, False)) if can else skip

        return go(root, True)
