from ren_check import ints
def validate(elevations, targets):
    ints("elevations", elevations, 3, 100_000, 0, 10**9)
    ints("targets", targets, 1, 100_000, 0, 10**9)
    t = elevations.index(max(elevations))
    assert 0 < t < len(elevations) - 1, "the top can't be at either end"
    assert all(elevations[i] < elevations[i + 1] for i in range(t)), "the trail must rise strictly to the top"
    assert all(elevations[i] > elevations[i + 1] for i in range(t, len(elevations) - 1)), "the trail must fall strictly after the top"
