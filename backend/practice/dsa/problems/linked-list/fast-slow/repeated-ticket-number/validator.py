def validate(tickets):
    assert isinstance(tickets, list), "tickets is a list"
    assert 2 <= len(tickets) <= 100_001, "2 <= tickets.length <= 10^5 + 1"
    n = len(tickets) - 1
    assert all(type(v) is int and 1 <= v <= n for v in tickets), "1 <= tickets[i] <= n"
    seen, reps = set(), set()
    for v in tickets:
        if v in seen:
            reps.add(v)
        seen.add(v)
    assert len(reps) == 1, "exactly one value appears more than once"
