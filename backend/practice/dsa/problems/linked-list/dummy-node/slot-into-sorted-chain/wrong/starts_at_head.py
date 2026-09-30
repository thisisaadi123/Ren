class Solution:
    # Mistake: starts the walk at the head itself, so the new node always lands after it.
    def insertSorted(self, head, value):
        if head is None:
            return ListNode(value)
        cur = head
        while cur.next and cur.next.val < value:
            cur = cur.next
        cur.next = ListNode(value, cur.next)
        return head
