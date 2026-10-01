def validate(posts, k):
    assert isinstance(posts, list) and 2 <= len(posts) <= 100_000, "2 <= posts.length <= 10^5"
    assert all(isinstance(p, list) and len(p) == 2 and all(type(v) is int and -10**8 <= v <= 10**8 for v in p) for p in posts), "each post is [x, y] within ±10^8"
    assert all(posts[i][0] < posts[i + 1][0] for i in range(len(posts) - 1)), "x is strictly increasing"
    assert type(k) is int and 0 <= k <= 2 * 10**8, "0 <= k <= 2 * 10^8"
    assert any(posts[i + 1][0] - posts[i][0] <= k for i in range(len(posts) - 1)), "some pair is close enough"
