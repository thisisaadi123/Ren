from ren_check import ints, integer
def validate(playlist, target):
    ints("playlist", playlist, 1, 100_000, -10**9, 10**9)
    assert len(set(playlist)) == len(playlist), "values are distinct"
    drops = sum(a > b for a, b in zip(playlist, playlist[1:]))
    assert drops == 0 or (drops == 1 and playlist[-1] < playlist[0]), "playlist must be a rotated sorted list"
    integer("target", target, -10**9, 10**9)
