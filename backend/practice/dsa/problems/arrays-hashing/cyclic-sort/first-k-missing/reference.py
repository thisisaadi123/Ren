class Solution:
    def firstMissing(self, nums, k):
        a = nums[:]
        n = len(a)
        i = 0
        while i < n:
            j = a[i] - 1
            if 0 <= j < n and a[i] != a[j]:
                a[i], a[j] = a[j], a[i]
            else:
                i += 1
        out = []
        extra = set()
        for i in range(n):
            if a[i] != i + 1:
                if len(out) < k:
                    out.append(i + 1)
                if a[i] > 0:
                    extra.add(a[i])
        x = n + 1
        while len(out) < k:
            if x not in extra:
                out.append(x)
            x += 1
        return out
