def validate(digits):
    assert type(digits) is str and 1 <= len(digits) <= 20 and digits.isdigit(), "1 <= length <= 20, digits only"
