class Solution:
    def deliveryRange(self, times, target):
        idx = [i for i, t in enumerate(times) if t == target]
        return [idx[0], idx[-1]] if idx else [-1, -1]
