class Solution:
    # For each person, scans the whole floor for cousins: O(width^2) per floor.
    def cousinSums(self, root):
        level, parent = [root], {id(root): None}
        answer = {id(root): 0}
        while level:
            vals = [(n, parent[id(n)], n.val) for n in level]
            for n, p, _ in vals:
                answer[id(n)] = sum(v for m, q, v in vals if q != p)
            nxt = []
            for n in level:
                for c in (n.left, n.right):
                    if c:
                        parent[id(c)] = id(n)
                        nxt.append(c)
            for n in level:
                n.val = answer[id(n)]
            level = nxt
        return root
