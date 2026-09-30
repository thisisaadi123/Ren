class Solution:
    def sortByDistance(self, head):
        vals = []
        while head:
            vals.append(head.val)
            head = head.next
        # Stable selection: repeatedly take the earliest value with the smallest distance.
        out_vals = []
        while vals:
            best = 0
            for i in range(1, len(vals)):
                if abs(vals[i]) < abs(vals[best]):
                    best = i
            out_vals.append(vals.pop(best))
        out = None
        for v in reversed(out_vals):
            out = ListNode(v, out)
        return out
