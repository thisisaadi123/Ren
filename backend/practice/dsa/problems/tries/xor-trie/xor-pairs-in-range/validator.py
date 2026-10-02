def validate(nums, low, high):
    assert isinstance(nums, list) and 1 <= len(nums) <= 20_000, "1 <= nums.length <= 2 * 10^4"
    assert all(type(v) is int and 1 <= v <= 20_000 for v in nums), "1 <= nums[i] <= 2 * 10^4"
    assert type(low) is int and type(high) is int and 1 <= low <= high <= 20_000, "1 <= low <= high <= 2 * 10^4"
