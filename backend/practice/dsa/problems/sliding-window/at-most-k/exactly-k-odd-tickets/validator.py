def validate(tickets, k):
    assert isinstance(tickets, list) and 1 <= len(tickets) <= 100_000, "1 <= tickets.length <= 10^5"
    assert all(type(v) is int and 1 <= v <= 10**5 for v in tickets), "1 <= tickets[i] <= 10^5"
    assert type(k) is int and 1 <= k <= len(tickets), "1 <= k <= tickets.length"
