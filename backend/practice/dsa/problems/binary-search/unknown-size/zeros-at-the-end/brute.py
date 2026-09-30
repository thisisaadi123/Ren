class Solution:
    def smallestWithZeros(self, zeros):
        n = count = 0
        while count < zeros:
            n += 1
            m = n
            while m % 5 == 0:
                count += 1
                m //= 5
        return n
