class Solution:
    def positionsAfter(self, head, steps):
        slow = fast = head
        looped = False
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                looped = True
                break
        vals = []
        if not looped:
            node = head
            while node:
                vals.append(node.val)
                node = node.next
            n = len(vals)
            return [vals[s] if s < n else -1 for s in steps]
        entry, mu = head, 0
        while entry is not slow:
            entry = entry.next
            slow = slow.next
            mu += 1
        lam, node = 1, entry.next
        while node is not entry:
            node = node.next
            lam += 1
        node = head
        for _ in range(mu + lam):
            vals.append(node.val)
            node = node.next
        return [vals[s] if s < mu + lam else vals[mu + (s - mu) % lam] for s in steps]
