def validate(headA, headB):
    assert isinstance(headA, list) and 1 <= len(headA) <= 30_000, "the first line has 1 to 3 * 10^4 stops"
    own = headB["values"] if isinstance(headB, dict) else headB
    assert isinstance(own, list) and len(own) <= 30_000, "the second line has at most 3 * 10^4 stops of its own"
    if isinstance(headB, dict):
        j = headB.get("join_at")
        assert type(j) is int and 0 <= j < len(headA), "join_at is a stop of the first line"
        assert set(headB) <= {"values", "join_at"}, "only values and join_at"
    else:
        assert own, "a second line that doesn't join needs at least one stop"
    vals = headA + own
    assert all(type(v) is int and 1 <= v <= 10**5 for v in vals), "1 <= stop number <= 10^5"
    assert len(set(vals)) == len(vals), "stop numbers are all different"
