class Solution:
    # Mistake: tracks invited ages in a set; removing one of two equal ages on the way back
    # forgets the other one is still invited.
    def feudFreeLists(self, ages, k):
        on = set()
        n = len(ages)
        total = 0
        def go(i):
            nonlocal total
            if i == n:
                total += 1
                return
            go(i + 1)
            a = ages[i]
            if a - k not in on and a + k not in on:
                had = a in on
                on.add(a)
                go(i + 1)
                on.discard(a)
        go(0)
        return total - 1
