from ren_check import ints
def validate(tickets):
    ints("tickets", tickets, 1, 100_000, 1, len(tickets))
