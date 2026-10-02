def validate(nums, queries):
    assert isinstance(nums, list) and 1 <= len(nums) <= 20_000, "1 <= nums.length <= 2 * 10^4"
    assert isinstance(queries, list) and 1 <= len(queries) <= 20_000, "1 <= queries.length <= 2 * 10^4"
    assert all(type(v) is int and 0 <= v <= 10**9 for v in nums), "0 <= nums[j] <= 10^9"
    assert all(isinstance(q, list) and len(q) == 2 and all(type(v) is int and 0 <= v <= 10**9 for v in q) for q in queries), "0 <= x, m <= 10^9"
