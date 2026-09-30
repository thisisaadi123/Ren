from ren_check import matrix
def validate(photo):
    matrix("photo", photo, 1, 500, 1, 500, -1000, 1000)
    assert len(photo[0]) == len(photo), "photo must be square"
