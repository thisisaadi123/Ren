class Solution:
    # Mistake: returns the last stop when both lines end at the same node, not the first shared one.
    def meetPoint(self, headA, headB):
        a, b = headA, headB
        while a.next:
            a = a.next
        while b and b.next:
            b = b.next
        return a if a is b else None
