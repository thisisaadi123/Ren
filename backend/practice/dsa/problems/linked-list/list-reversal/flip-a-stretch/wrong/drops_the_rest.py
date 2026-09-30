class Solution:
    # Mistake: reverses the stretch but never reconnects the nodes after `right`.
    def flipStretch(self, head, left, right):
        dummy = ListNode(0, head)
        before = dummy
        for _ in range(left - 1):
            before = before.next
        prev, cur = None, before.next
        for _ in range(right - left + 1):
            cur.next, prev, cur = prev, cur, cur.next
        before.next = prev
        return dummy.next
