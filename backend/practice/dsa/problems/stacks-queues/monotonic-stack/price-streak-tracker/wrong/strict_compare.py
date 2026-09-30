class PriceStreak:
    # Mistake: stops at an equal price, so equal days don't join the streak.
    def __init__(self):
        self.st = []

    def record(self, price):
        streak = 1
        while self.st and self.st[-1][0] < price:
            streak += self.st.pop()[1]
        self.st.append((price, streak))
        return streak
