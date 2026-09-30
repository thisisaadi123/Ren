class Solution:
    def feudFreeLists(self, ages, k):
        cnt = collections.Counter()
        n = len(ages)
        total = 0

        def go(i):
            nonlocal total
            if i == n:
                total += 1
                return
            go(i + 1)
            a = ages[i]
            if cnt[a - k] == 0 and cnt[a + k] == 0:
                cnt[a] += 1
                go(i + 1)
                cnt[a] -= 1

        go(0)
        return total - 1
