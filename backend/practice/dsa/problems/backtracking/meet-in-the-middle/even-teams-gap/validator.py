def validate(skills):
    assert isinstance(skills, list) and 2 <= len(skills) <= 30 and len(skills) % 2 == 0, "skills.length = 2n with 1 <= n <= 15"
    assert all(type(x) is int and -10**7 <= x <= 10**7 for x in skills), "-10^7 <= skills[i] <= 10^7"
