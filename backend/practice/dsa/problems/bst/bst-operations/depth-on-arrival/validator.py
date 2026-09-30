from ren_check import ints


def validate(keys):
    ints("keys", keys, 1, 10**5, -10**9, 10**9)
    assert len(set(keys)) == len(keys), "all keys are distinct"
