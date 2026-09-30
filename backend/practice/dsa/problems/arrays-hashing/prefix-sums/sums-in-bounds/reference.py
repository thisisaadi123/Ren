class Solution:
    def countSumsInBounds(self, nums, lower, upper):
        prefix = [0]
        for x in nums:
            prefix.append(prefix[-1] + x)

        def sort_count(a):
            if len(a) <= 1:
                return a, 0
            mid = len(a) // 2
            left, c1 = sort_count(a[:mid])
            right, c2 = sort_count(a[mid:])
            count = c1 + c2
            lo = hi = 0
            for p in left:
                while lo < len(right) and right[lo] - p < lower:
                    lo += 1
                while hi < len(right) and right[hi] - p <= upper:
                    hi += 1
                count += hi - lo
            merged, i, j = [], 0, 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    merged.append(left[i]); i += 1
                else:
                    merged.append(right[j]); j += 1
            merged += left[i:] + right[j:]
            return merged, count

        return sort_count(prefix)[1]
