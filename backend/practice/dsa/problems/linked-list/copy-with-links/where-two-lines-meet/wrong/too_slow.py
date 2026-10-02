class Solution:
    # Mistake: for every stop of the second line, walks the whole first line: O(n * m).
    def meetPoint(self, headA, headB):
        b = headB
        while b:
            a = headA
            while a:
                if a is b:
                    return a
                a = a.next
            b = b.next
        return None
