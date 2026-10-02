def validate(nums):
    assert isinstance(nums, list) and 1 <= len(nums) <= 20_000, "1 <= nums.length <= 2 * 10^4"
    assert all(type(v) is int and 0 <= v <= 2**31 - 1 for v in nums), "0 <= nums[i] <= 2^31 - 1"
