def validate(cards):
    assert isinstance(cards, list) and 1 <= len(cards) <= 100_000, "1 <= cards.length <= 10^5"
    assert all(type(v) is int and 1 <= v <= 10**9 for v in cards), "1 <= cards[i] <= 10^9"
    assert len(set(cards)) == len(cards), "cards are distinct"
