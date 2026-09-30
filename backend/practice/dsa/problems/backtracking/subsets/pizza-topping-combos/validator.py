from ren_check import ints
def validate(toppings):
    ints("toppings", toppings, 1, 10, -10, 10)
    assert len(set(toppings)) == len(toppings), "toppings are distinct"
