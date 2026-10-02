def validate(nums, goal):
    assert isinstance(nums, list) and 1 <= len(nums) <= 36, "1 <= nums.length <= 36"
    assert all(type(x) is int and -10**7 <= x <= 10**7 for x in nums), "-10^7 <= nums[i] <= 10^7"
    assert type(goal) is int and -10**9 <= goal <= 10**9, "-10^9 <= goal <= 10^9"
