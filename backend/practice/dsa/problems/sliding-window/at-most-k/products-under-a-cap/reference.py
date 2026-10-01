class Solution:
    def countUnderCap(self, factors, cap):
        if cap <= 1:
            return 0
        product = 1
        left = total = 0
        for i, f in enumerate(factors):
            product *= f
            while product >= cap:
                product //= factors[left]
                left += 1
            total += i - left + 1
        return total
