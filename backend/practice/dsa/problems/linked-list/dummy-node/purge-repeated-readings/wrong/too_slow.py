class Solution:
    # Mistake: counts each value by rescanning the whole list, O(n^2).
    def purgeRepeats(self, head):
        dummy = ListNode(0)
        tail = dummy
        cur = head
        while cur:
            seen = 0
            scan = head
            while scan:
                if scan.val == cur.val:
                    seen += 1
                scan = scan.next
            if seen == 1:
                tail.next = ListNode(cur.val)
                tail = tail.next
            cur = cur.next
        return dummy.next
