class Solution:
    # Mistake: walks both lists in step without lining them up, so lines of different lengths never meet.
    def meetPoint(self, headA, headB):
        a, b = headA, headB
        while a and b:
            if a is b:
                return a
            a, b = a.next, b.next
        return None
