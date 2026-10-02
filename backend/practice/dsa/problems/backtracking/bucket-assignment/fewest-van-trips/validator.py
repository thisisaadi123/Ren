def validate(boxes, capacity):
    assert isinstance(boxes, list) and 1 <= len(boxes) <= 14, "1 <= boxes.length <= 14"
    assert type(capacity) is int and 1 <= capacity <= 10**6, "capacity <= 10^6"
    assert all(type(x) is int and 1 <= x <= capacity for x in boxes), "1 <= boxes[i] <= capacity"
