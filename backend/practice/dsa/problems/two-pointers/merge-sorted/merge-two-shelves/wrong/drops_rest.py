class Solution:
    # Mistake: forgets the leftover books.
    def mergeShelves(self, left, right):
        out = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                out.append(left[i]); i += 1
            else:
                out.append(right[j]); j += 1
        return out
