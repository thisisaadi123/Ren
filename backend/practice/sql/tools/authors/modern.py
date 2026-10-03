"""Intervals & overlaps, product analytics and JSON data."""
import json

import _common  # noqa: F401
from author import FIRST, P, T, day, done, firsts, maybe
from worlds import ties

# --- Intervals & overlaps -------------------------------------------------------------------------

BOOKINGS = T("bookings", ("id", "INTEGER", "pk"), ("room", "TEXT"), ("check_in", "TEXT"), ("check_out", "TEXT"))
ROOMS = ["101", "102", "201", "202", "301"]


def bookings_gen(rng, n, k):
    rooms = ROOMS[: max(1, min(5, n // 3 + 1))]
    rows = []
    for i in range(n + 1):
        start = rng.randint(0, max(3, n))
        rows.append((i + 1, rng.choice(rooms), day(start), day(start + rng.randint(1, 4))))
    return {"bookings": rows}

P("double-booked-rooms", "Double-booked Rooms", "intervals", "overlap-checks", "medium",
  """
  A booking holds its room from `check_in` up to, but not including, `check_out` (the next guest can check in on the
  day the last one checks out). Find every pair of bookings for the **same room** that overlap.

  Return `first_id` and `second_id` (the smaller id first) for each such pair, in any order.
  """,
  [BOOKINGS],
  """
  SELECT a.id AS first_id, b.id AS second_id
  FROM bookings a
  JOIN bookings b ON b.room = a.room AND a.id < b.id
  WHERE a.check_in < b.check_out AND b.check_in < a.check_out
  """,
  [({"bookings": [(1, "101", "2024-05-01", "2024-05-04"), (2, "101", "2024-05-03", "2024-05-05"), (3, "101", "2024-05-05", "2024-05-07"), (4, "102", "2024-05-02", "2024-05-06")]},
    "Bookings 1 and 2 both hold room 101 on May 3. Booking 3 checks in the day booking 2 checks out, which is fine. Booking 4 is another room.")],
  bookings_gen,
  wrong=["SELECT a.id AS first_id, b.id AS second_id FROM bookings a JOIN bookings b ON b.room = a.room AND a.id < b.id WHERE a.check_in <= b.check_out AND b.check_in <= a.check_out",
         "SELECT a.id AS first_id, b.id AS second_id FROM bookings a JOIN bookings b ON b.room = a.room AND a.id < b.id WHERE b.check_in BETWEEN a.check_in AND a.check_out"],
  notes="Two ranges overlap exactly when each one starts before the other ends.",
  sizes=[2, 3, 4, 6, 8, 10, 14, 20, 30, 45, 70, 120])

PEOPLE = T("people", ("name", "TEXT", "pk"))
MEETINGS = T("meetings", ("name", "TEXT", "fk people.name"), ("starts_at", "TEXT"), ("ends_at", "TEXT"))


def meetings_gen(rng, n, k):
    people = firsts(rng, max(2, n // 2 + 2))
    rows = []
    for _ in range(n):
        s = rng.choice([12, 13, 14, 15]) * 60 + rng.choice([0, 30]) if ties(k) else rng.randint(9 * 60, 17 * 60)
        e = s + rng.choice([30, 60, 90])
        rows.append((rng.choice(people), f"{s // 60:02d}:{s % 60:02d}", f"{e // 60:02d}:{e % 60:02d}"))
    return {"people": [(p,) for p in people], "meetings": rows}

P("free-for-the-review", "Free for the Review", "intervals", "overlap-checks", "medium",
  """
  A review is set for **14:00 to 15:00**. Times are written `HH:MM` and a meeting holds its time from `starts_at` up to,
  but not including, `ends_at`. Someone is **free** if none of their meetings overlap the review (a meeting ending at
  14:00 or starting at 15:00 is fine).

  Return the `name` of everyone who is free, ordered by `name`.
  """,
  [PEOPLE, MEETINGS],
  """
  SELECT p.name FROM people p
  WHERE NOT EXISTS (
    SELECT 1 FROM meetings m
    WHERE m.name = p.name AND m.starts_at < '15:00' AND m.ends_at > '14:00'
  )
  ORDER BY p.name
  """,
  [({"people": [("Kai",), ("Lena",), ("Mina",), ("Noor",)],
     "meetings": [("Kai", "13:00", "14:00"), ("Lena", "14:30", "15:30"), ("Mina", "13:30", "16:00"), ("Noor", "15:00", "15:30")]},
    "Kai's meeting ends right as the review starts and Noor's starts right as it ends, so both are free. Lena's and Mina's overlap it.")],
  meetings_gen,
  ordered=True,
  wrong=["SELECT p.name FROM people p WHERE NOT EXISTS (SELECT 1 FROM meetings m WHERE m.name = p.name AND m.starts_at >= '14:00' AND m.starts_at < '15:00') ORDER BY p.name",
         "SELECT p.name FROM people p WHERE NOT EXISTS (SELECT 1 FROM meetings m WHERE m.name = p.name AND m.starts_at <= '15:00' AND m.ends_at >= '14:00') ORDER BY p.name"],
  notes="Times written as `HH:MM` with leading zeros compare correctly as text.")

BUSY = T("busy", ("person", "TEXT"), ("start_min", "INTEGER"), ("end_min", "INTEGER"))


def busy_gen(rng, n, k):
    rows = []
    for p in firsts(rng, max(1, n // 4 + 1)):
        for _ in range(rng.randint(1, max(1, n // 2))):
            s = rng.randint(0, 100) * 5
            rows.append((p, s, s + rng.choice([5, 10, 15]) if ties(k) else s + rng.randint(1, 120)))
    rng.shuffle(rows)
    return {"busy": rows}

P("merge-busy-times", "Merge Busy Times", "intervals", "merge-ranges", "hard",
  """
  `busy` lists blocks of time (in minutes) when people are busy, from `start_min` to `end_min`. Blocks can overlap or
  touch. For each person, merge their blocks: blocks that overlap or touch (one ends exactly when the next starts)
  become one.

  Return `person`, `start_min` and `end_min` of each merged block, ordered by `person`, then `start_min`.
  """,
  [BUSY],
  """
  WITH ordered AS (
    SELECT person, start_min, end_min,
           MAX(end_min) OVER (PARTITION BY person ORDER BY start_min, end_min
                              ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS reach
    FROM busy
  ),
  grouped AS (
    SELECT person, start_min, end_min,
           SUM(CASE WHEN reach IS NULL OR start_min > reach THEN 1 ELSE 0 END)
             OVER (PARTITION BY person ORDER BY start_min, end_min ROWS UNBOUNDED PRECEDING) AS block
    FROM ordered
  )
  SELECT person, MIN(start_min) AS start_min, MAX(end_min) AS end_min
  FROM grouped
  GROUP BY person, block
  ORDER BY person, start_min
  """,
  [({"busy": [("Kai", 60, 120), ("Kai", 90, 100), ("Kai", 110, 150), ("Kai", 150, 160), ("Kai", 200, 230), ("Lena", 10, 20)]},
    "Kai's 60–120 block contains 90–100, overlaps 110–150, and 150–160 touches it: together 60–160. 200–230 stands alone.")],
  busy_gen,
  ordered=True,
  wrong=["WITH ordered AS (SELECT person, start_min, end_min, LAG(end_min) OVER (PARTITION BY person ORDER BY start_min, end_min) AS reach FROM busy), grouped AS (SELECT person, start_min, end_min, SUM(CASE WHEN reach IS NULL OR start_min > reach THEN 1 ELSE 0 END) OVER (PARTITION BY person ORDER BY start_min, end_min ROWS UNBOUNDED PRECEDING) AS block FROM ordered) SELECT person, MIN(start_min) AS start_min, MAX(end_min) AS end_min FROM grouped GROUP BY person, block ORDER BY person, start_min",
         "WITH ordered AS (SELECT person, start_min, end_min, MAX(end_min) OVER (PARTITION BY person ORDER BY start_min, end_min ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS reach FROM busy), grouped AS (SELECT person, start_min, end_min, SUM(CASE WHEN reach IS NULL OR start_min >= reach THEN 1 ELSE 0 END) OVER (PARTITION BY person ORDER BY start_min, end_min ROWS UNBOUNDED PRECEDING) AS block FROM ordered) SELECT person, MIN(start_min) AS start_min, MAX(end_min) AS end_min FROM grouped GROUP BY person, block ORDER BY person, start_min"],
  notes="Compare each block with the furthest end reached by any earlier block (a running `MAX`), not just the previous block: a long block can cover several later ones.")

CAMPAIGNS = T("campaigns", ("id", "INTEGER", "pk"), ("start_day", "TEXT"), ("end_day", "TEXT"))


def campaigns_gen(rng, n, k):
    rows = []
    for i in range(n + 1):
        s = rng.randint(0, max(5, n * 2))
        rows.append((i + 1, day(s), day(s + rng.randint(0, 6))))
    return {"campaigns": rows}

P("days-with-a-campaign", "Days with a Campaign", "intervals", "merge-ranges", "hard",
  """
  Each marketing campaign runs from `start_day` to `end_day`, **both included**. Campaigns can overlap.

  Return one row with `days`: how many different calendar days had at least one campaign running.
  """,
  [CAMPAIGNS],
  """
  WITH ordered AS (
    SELECT julianday(start_day) AS s, julianday(end_day) AS e,
           MAX(julianday(end_day)) OVER (ORDER BY start_day, end_day ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS reach
    FROM campaigns
  ),
  grouped AS (
    SELECT s, e, SUM(CASE WHEN reach IS NULL OR s > reach THEN 1 ELSE 0 END) OVER (ORDER BY s, e ROWS UNBOUNDED PRECEDING) AS block
    FROM ordered
  )
  SELECT CAST(SUM(last - first + 1) AS INTEGER) AS days
  FROM (SELECT MIN(s) AS first, MAX(e) AS last FROM grouped GROUP BY block)
  """,
  [({"campaigns": [(1, "2024-06-01", "2024-06-05"), (2, "2024-06-04", "2024-06-08"), (3, "2024-06-12", "2024-06-12")]},
    "The first two campaigns together cover June 1–8 (8 days, not 5 + 5 = 10). The third adds June 12: 9 days.")],
  campaigns_gen,
  wrong=["SELECT CAST(SUM(julianday(end_day) - julianday(start_day) + 1) AS INTEGER) AS days FROM campaigns",
         "SELECT CAST(julianday(MAX(end_day)) - julianday(MIN(start_day)) + 1 AS INTEGER) AS days FROM campaigns"])

STAYS = T("stays", ("guest", "TEXT"), ("check_in", "TEXT"), ("check_out", "TEXT"))


def stays_gen(rng, n, k):
    rows = []
    for g in firsts(rng, n):
        s = rng.randint(0, max(3, n // 2))
        rows.append((g, day(s), day(s + rng.randint(1, 5))))
    return {"stays": rows}

P("fullest-night", "The Fullest Night", "intervals", "peak-concurrency", "hard",
  """
  A guest stays from `check_in` up to, but not including, `check_out`: they're in the hotel the nights of `check_in`
  through the day before `check_out`.

  Return one row with `peak`: the largest number of guests in the hotel on the same night.
  """,
  [STAYS],
  """
  WITH events AS (
    SELECT check_in AS d, 1 AS delta FROM stays
    UNION ALL
    SELECT check_out, -1 FROM stays
  ),
  running AS (
    SELECT SUM(delta) OVER (ORDER BY d, delta ROWS UNBOUNDED PRECEDING) AS guests FROM events
  )
  SELECT MAX(guests) AS peak FROM running
  """,
  [({"stays": [("Kai", "2024-07-01", "2024-07-04"), ("Lena", "2024-07-02", "2024-07-03"), ("Mina", "2024-07-03", "2024-07-05"), ("Noor", "2024-07-04", "2024-07-06")]},
    "On July 2, Kai and Lena are in. On July 3, Lena has left and Mina arrived: still 2. On July 4, Kai has left: Mina and Noor. No night has 3.")],
  stays_gen,
  wrong=["WITH events AS (SELECT check_in AS d, 1 AS delta FROM stays UNION ALL SELECT check_out, -1 FROM stays), running AS (SELECT SUM(delta) OVER (ORDER BY d, delta DESC ROWS UNBOUNDED PRECEDING) AS guests FROM events) SELECT MAX(guests) AS peak FROM running",
         "SELECT MAX(n) AS peak FROM (SELECT COUNT(*) AS n FROM stays GROUP BY check_in)"],
  notes="Turn each stay into +1 on arrival and −1 on departure, sort, and keep a running sum. On the same day, departures go first, since that guest's room is free that night.")

CALLS = T("calls", ("id", "INTEGER", "pk"), ("day", "TEXT"), ("start_min", "INTEGER"), ("end_min", "INTEGER"))


def calls_gen(rng, n, k):
    rows = []
    for i in range(n + 1):
        s = rng.randint(0, 60 if ties(k) else 600)
        rows.append((i + 1, day(rng.randint(0, max(1, n // 6))), s, s + rng.randint(1, 30)))
    return {"calls": rows}

P("peak-calls-per-day", "Peak Calls per Day", "intervals", "peak-concurrency", "medium",
  """
  Each call lasts from `start_min` up to, but not including, `end_min` (minutes since midnight). For each day with calls,
  find the most calls that were going on at the same moment.

  Return `day` and `peak`, ordered by `day`.
  """,
  [CALLS],
  """
  WITH events AS (
    SELECT day, start_min AS t, 1 AS delta FROM calls
    UNION ALL
    SELECT day, end_min, -1 FROM calls
  ),
  running AS (
    SELECT day, SUM(delta) OVER (PARTITION BY day ORDER BY t, delta ROWS UNBOUNDED PRECEDING) AS active FROM events
  )
  SELECT day, MAX(active) AS peak FROM running GROUP BY day ORDER BY day
  """,
  [({"calls": [(1, "2024-08-01", 0, 10), (2, "2024-08-01", 5, 15), (3, "2024-08-01", 10, 20), (4, "2024-08-02", 30, 40)]},
    "On August 1, calls 1 and 2 overlap from minute 5 to 10. Call 3 starts as call 1 ends, so it never makes 3. August 2 has one call.")],
  calls_gen,
  ordered=True,
  wrong=["WITH events AS (SELECT day, start_min AS t, 1 AS delta FROM calls UNION ALL SELECT day, end_min, -1 FROM calls), running AS (SELECT day, SUM(delta) OVER (ORDER BY t, delta ROWS UNBOUNDED PRECEDING) AS active FROM events) SELECT day, MAX(active) AS peak FROM running GROUP BY day ORDER BY day",
         "WITH events AS (SELECT day, start_min AS t, 1 AS delta FROM calls UNION ALL SELECT day, end_min, -1 FROM calls), running AS (SELECT day, SUM(delta) OVER (PARTITION BY day ORDER BY t, delta DESC ROWS UNBOUNDED PRECEDING) AS active FROM events) SELECT day, MAX(active) AS peak FROM running GROUP BY day ORDER BY day"])

# --- Product analytics ----------------------------------------------------------------------------

EVENTS = T("events", ("user_id", "INTEGER"), ("event", "TEXT"), ("at", "TEXT"))
STEPS = ["view", "cart", "checkout", "paid"]


def funnel_gen(rng, n, k):
    rows = []
    for u in range(1, n + 2):
        t = rng.randint(0, 2000)
        depth = rng.choice([1, 1, 2, 2, 3, 4])
        for step in STEPS[:depth]:
            for _ in range(rng.choice([1, 1, 2])):
                rows.append((u, step, f"2024-09-{1 + t // 1440:02d} {t % 1440 // 60:02d}:{t % 60:02d}"))
                t += rng.randint(0 if ties(k) else 1, 20)
        if rng.random() < 0.2:  # a stray step out of order
            rows.append((u, rng.choice(STEPS), f"2024-09-01 00:{rng.randint(0, 59):02d}"))
    rng.shuffle(rows)
    return {"events": rows}

P("checkout-funnel", "Checkout Funnel", "product-analytics", "funnels", "medium",
  """
  The checkout has four steps: `'view'`, `'cart'`, `'checkout'` and `'paid'`. Users can repeat a step.

  Return one row per step, **in that order**, with `step` and `users` (how many different users did that step at least
  once). A step nobody reached still appears, with 0.
  """,
  [EVENTS],
  """
  WITH steps(step, pos) AS (VALUES ('view', 1), ('cart', 2), ('checkout', 3), ('paid', 4))
  SELECT s.step, COUNT(DISTINCT e.user_id) AS users
  FROM steps s
  LEFT JOIN events e ON e.event = s.step
  GROUP BY s.step, s.pos
  ORDER BY s.pos
  """,
  [({"events": [(1, "view", "2024-09-01 10:00"), (1, "view", "2024-09-01 10:02"), (1, "cart", "2024-09-01 10:05"), (2, "view", "2024-09-01 11:00"), (3, "view", "2024-09-01 12:00"), (3, "cart", "2024-09-01 12:03")]},
    "Three users viewed (user 1 twice), two added to the cart, and nobody checked out or paid.")],
  funnel_gen,
  ordered=True,
  wrong=["SELECT event AS step, COUNT(DISTINCT user_id) AS users FROM events GROUP BY event ORDER BY step",
         "WITH steps(step, pos) AS (VALUES ('view', 1), ('cart', 2), ('checkout', 3), ('paid', 4)) SELECT s.step, COUNT(e.user_id) AS users FROM steps s LEFT JOIN events e ON e.event = s.step GROUP BY s.step, s.pos ORDER BY s.pos"],
  notes="`VALUES` can build a small table of your own inside a `WITH`.")

P("strict-funnel", "Strict Funnel", "product-analytics", "funnels", "hard",
  """
  A strict funnel only counts steps taken **in order**. A user has **viewed** if they have any `'view'`; they've
  **carted** if they have a `'cart'` strictly later than their first view; they've **paid** if they have a `'paid'`
  strictly later than their first such cart. (`'checkout'` is ignored here.)

  Return one row: `viewed`, `carted` and `paid` (numbers of users).
  """,
  [EVENTS],
  """
  WITH viewed AS (
    SELECT user_id, MIN(at) AS t FROM events WHERE event = 'view' GROUP BY user_id
  ),
  carted AS (
    SELECT v.user_id, MIN(e.at) AS t
    FROM viewed v JOIN events e ON e.user_id = v.user_id AND e.event = 'cart' AND e.at > v.t
    GROUP BY v.user_id
  ),
  paid AS (
    SELECT DISTINCT c.user_id
    FROM carted c JOIN events e ON e.user_id = c.user_id AND e.event = 'paid' AND e.at > c.t
  )
  SELECT (SELECT COUNT(*) FROM viewed) AS viewed,
         (SELECT COUNT(*) FROM carted) AS carted,
         (SELECT COUNT(*) FROM paid) AS paid
  """,
  [({"events": [(1, "view", "2024-09-01 10:00"), (1, "cart", "2024-09-01 10:05"), (1, "paid", "2024-09-01 10:09"),
                (2, "cart", "2024-09-01 09:00"), (2, "view", "2024-09-01 09:30"), (2, "paid", "2024-09-01 09:40"),
                (3, "view", "2024-09-01 12:00"), (3, "cart", "2024-09-01 12:00")]},
    "All three viewed. User 2 carted before viewing, and user 3's cart has the same time as the view, not later, so only user 1 carted and paid.")],
  funnel_gen,
  wrong=["SELECT COUNT(DISTINCT CASE WHEN event = 'view' THEN user_id END) AS viewed, COUNT(DISTINCT CASE WHEN event = 'cart' THEN user_id END) AS carted, COUNT(DISTINCT CASE WHEN event = 'paid' THEN user_id END) AS paid FROM events",
         "WITH viewed AS (SELECT user_id, MIN(at) AS t FROM events WHERE event = 'view' GROUP BY user_id), carted AS (SELECT v.user_id, MIN(e.at) AS t FROM viewed v JOIN events e ON e.user_id = v.user_id AND e.event = 'cart' AND e.at >= v.t GROUP BY v.user_id), paid AS (SELECT DISTINCT c.user_id FROM carted c JOIN events e ON e.user_id = c.user_id AND e.event = 'paid' AND e.at >= c.t) SELECT (SELECT COUNT(*) FROM viewed) AS viewed, (SELECT COUNT(*) FROM carted) AS carted, (SELECT COUNT(*) FROM paid) AS paid"])

ASSIGN = T("assignments", ("user_id", "INTEGER", "pk"), ("variant", "TEXT"))
PURCHASES = T("purchases", ("user_id", "INTEGER", "fk assignments.user_id"), ("amount", "REAL"))


def ab_gen(rng, n, k):
    users = [(u, "A" if u % 2 else "B") if ties(k) else (u, rng.choice("AB")) for u in range(1, n + 3)]
    users[0], users[1] = (1, "A"), (2, "B")
    buys = []
    for u, v in users:
        if rng.random() < (0.3 if v == "A" else 0.4):
            for _ in range(rng.randint(1, 3)):
                buys.append((u, round(rng.choice([10, 20]) if ties(k) else rng.uniform(5, 80), 2)))
    buys.append((1, 15.0))  # group A always has some revenue
    return {"assignments": users, "purchases": buys}

P("conversion-by-variant", "Conversion by Variant", "product-analytics", "experiments", "medium",
  """
  Users were split into variants `'A'` and `'B'`. A user **converted** if they made at least one purchase (some made
  several).

  For each variant, return `variant`, `users` (assigned to it), `buyers` (users who converted) and `conversion`
  (buyers as a percentage of users, rounded to 1 decimal place). Order by `variant`.
  """,
  [ASSIGN, PURCHASES],
  """
  SELECT a.variant,
         COUNT(*) AS users,
         SUM(EXISTS (SELECT 1 FROM purchases p WHERE p.user_id = a.user_id)) AS buyers,
         ROUND(100.0 * SUM(EXISTS (SELECT 1 FROM purchases p WHERE p.user_id = a.user_id)) / COUNT(*), 1) AS conversion
  FROM assignments a
  GROUP BY a.variant
  ORDER BY a.variant
  """,
  [({"assignments": [(1, "A"), (2, "B"), (3, "A"), (4, "B"), (5, "B")], "purchases": [(1, 20.0), (1, 5.0), (2, 12.0), (5, 30.0)]},
    "In A, user 1 bought (twice) and user 3 didn't: 1 of 2 is 50.0%. In B, users 2 and 5 bought: 2 of 3 is 66.7%.")],
  ab_gen,
  ordered=True,
  wrong=["SELECT a.variant, COUNT(*) AS users, COUNT(p.user_id) AS buyers, ROUND(100.0 * COUNT(p.user_id) / COUNT(*), 1) AS conversion FROM assignments a LEFT JOIN purchases p ON p.user_id = a.user_id GROUP BY a.variant ORDER BY a.variant",
         "SELECT a.variant, COUNT(DISTINCT a.user_id) AS users, COUNT(DISTINCT p.user_id) AS buyers, ROUND(100.0 * COUNT(DISTINCT p.user_id) / COUNT(DISTINCT a.user_id), 1) AS conversion FROM assignments a JOIN purchases p ON p.user_id = a.user_id GROUP BY a.variant ORDER BY a.variant"])

P("revenue-lift", "Revenue Lift", "product-analytics", "experiments", "hard",
  """
  Compare the variants by **revenue per assigned user**: a variant's total purchase amount divided by everyone assigned
  to it, buyers or not.

  Return one row: `a_per_user` and `b_per_user` (each rounded to 2 decimal places) and `lift_pct`, B's change over A as a
  percentage of A, rounded to 1 decimal place (computed from the unrounded values).
  """,
  [ASSIGN, PURCHASES],
  """
  WITH per_variant AS (
    SELECT a.variant,
           1.0 * COALESCE((SELECT SUM(p.amount) FROM purchases p JOIN assignments x ON x.user_id = p.user_id WHERE x.variant = a.variant), 0) / COUNT(*) AS rpu
    FROM assignments a
    GROUP BY a.variant
  )
  SELECT ROUND(a.rpu, 2) AS a_per_user, ROUND(b.rpu, 2) AS b_per_user, ROUND(100.0 * (b.rpu - a.rpu) / a.rpu, 1) AS lift_pct
  FROM per_variant a JOIN per_variant b ON a.variant = 'A' AND b.variant = 'B'
  """,
  [({"assignments": [(1, "A"), (2, "B"), (3, "A"), (4, "B"), (5, "B")], "purchases": [(1, 20.0), (1, 5.0), (2, 12.0), (5, 30.0)]},
    "A takes 25.00 over 2 users: 12.50 each. B takes 42.00 over 3 users: 14.00 each. That's 1.50 more, a lift of 12.0%.")],
  ab_gen,
  wrong=["WITH per_variant AS (SELECT a.variant, AVG(p.amount) AS rpu FROM assignments a JOIN purchases p ON p.user_id = a.user_id GROUP BY a.variant) SELECT ROUND(a.rpu, 2) AS a_per_user, ROUND(b.rpu, 2) AS b_per_user, ROUND(100.0 * (b.rpu - a.rpu) / a.rpu, 1) AS lift_pct FROM per_variant a JOIN per_variant b ON a.variant = 'A' AND b.variant = 'B'",
         "WITH per_variant AS (SELECT a.variant, 1.0 * SUM(p.amount) / COUNT(DISTINCT p.user_id) AS rpu FROM assignments a JOIN purchases p ON p.user_id = a.user_id GROUP BY a.variant) SELECT ROUND(a.rpu, 2) AS a_per_user, ROUND(b.rpu, 2) AS b_per_user, ROUND(100.0 * (b.rpu - a.rpu) / a.rpu, 1) AS lift_pct FROM per_variant a JOIN per_variant b ON a.variant = 'A' AND b.variant = 'B'"])

LOGINS = T("logins", ("user_id", "INTEGER"), ("login_on", "TEXT"))


def sticky_gen(rng, n, k):
    rows = []
    users = max(2, n // 3 + 2)
    for _ in range(n * 2 + 2):
        rows.append((rng.randint(1, users), day(rng.randint(0, 75))))
    return {"logins": rows}

P("stickiness", "Stickiness", "product-analytics", "activity-metrics", "hard",
  """
  For each month (written `YYYY-MM`) with logins:

  - `mau`: monthly active users, the different users who logged in that month
  - `avg_dau`: the average number of different users per day, over the days of that month that had any login, rounded
    to 2 decimal places
  - `stickiness`: `avg_dau` as a percentage of `mau`, rounded to 1 decimal place (from the unrounded average)

  A user can log in several times a day. Order by `month`.
  """,
  [LOGINS],
  """
  WITH daily AS (
    SELECT login_on, COUNT(DISTINCT user_id) AS dau FROM logins GROUP BY login_on
  ),
  monthly AS (
    SELECT strftime('%Y-%m', login_on) AS month, COUNT(DISTINCT user_id) AS mau FROM logins GROUP BY month
  )
  SELECT m.month, m.mau,
         ROUND(AVG(d.dau), 2) AS avg_dau,
         ROUND(100.0 * AVG(d.dau) / m.mau, 1) AS stickiness
  FROM monthly m
  JOIN daily d ON strftime('%Y-%m', d.login_on) = m.month
  GROUP BY m.month, m.mau
  ORDER BY m.month
  """,
  [({"logins": [(1, "2024-01-02"), (2, "2024-01-02"), (1, "2024-01-02"), (1, "2024-01-03"), (3, "2024-01-20"), (1, "2024-02-01")]},
    "January has 3 active users. Its login days had 2, 1 and 1 users: 1.33 a day on average, which is 44.4% of 3.")],
  sticky_gen,
  ordered=True,
  wrong=["WITH daily AS (SELECT login_on, COUNT(*) AS dau FROM logins GROUP BY login_on), monthly AS (SELECT strftime('%Y-%m', login_on) AS month, COUNT(DISTINCT user_id) AS mau FROM logins GROUP BY month) SELECT m.month, m.mau, ROUND(AVG(d.dau), 2) AS avg_dau, ROUND(100.0 * AVG(d.dau) / m.mau, 1) AS stickiness FROM monthly m JOIN daily d ON strftime('%Y-%m', d.login_on) = m.month GROUP BY m.month, m.mau ORDER BY m.month",
         "WITH daily AS (SELECT login_on, COUNT(DISTINCT user_id) AS dau FROM logins GROUP BY login_on), monthly AS (SELECT strftime('%Y-%m', login_on) AS month, COUNT(*) AS mau FROM logins GROUP BY month) SELECT m.month, m.mau, ROUND(AVG(d.dau), 2) AS avg_dau, ROUND(100.0 * AVG(d.dau) / m.mau, 1) AS stickiness FROM monthly m JOIN daily d ON strftime('%Y-%m', d.login_on) = m.month GROUP BY m.month, m.mau ORDER BY m.month"])

DELIVERIES = T("deliveries", ("id", "INTEGER", "pk"), ("customer_id", "INTEGER"), ("ordered_on", "TEXT"), ("wanted_on", "TEXT"))


def deliveries_gen(rng, n, k):
    rows = []
    for i in range(n + 2):
        o = rng.randint(0, 3 if ties(k) else 30)
        rows.append((i + 1, rng.randint(1, max(1, n // 2 + 1)), day(o), day(o + rng.choice([0, 0, 1, 2]))))
    rng.shuffle(rows)
    return {"deliveries": rows}

P("instant-first-orders", "Instant First Orders", "product-analytics", "activity-metrics", "medium",
  """
  An order is **instant** if the customer wanted it the day they ordered (`wanted_on = ordered_on`). A customer's
  **first** order is their earliest by `ordered_on`, then smallest `id`.

  Return one row with `instant_pct`: the percentage of customers whose first order was instant, rounded to 2 decimal
  places.
  """,
  [DELIVERIES],
  """
  WITH firsts AS (
    SELECT ordered_on, wanted_on,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY ordered_on, id) AS rn
    FROM deliveries
  )
  SELECT ROUND(100.0 * SUM(wanted_on = ordered_on) / COUNT(*), 2) AS instant_pct
  FROM firsts
  WHERE rn = 1
  """,
  [({"deliveries": [(1, 1, "2024-08-01", "2024-08-02"), (2, 2, "2024-08-02", "2024-08-02"), (3, 1, "2024-08-03", "2024-08-03"), (4, 3, "2024-08-03", "2024-08-03"), (5, 3, "2024-08-03", "2024-08-04")]},
    "Customer 1's first order (id 1) wasn't instant. Customer 2's was. Customer 3 ordered twice on August 3; the first by id (4) was instant. That's 2 of 3: 66.67%.")],
  deliveries_gen,
  wrong=["SELECT ROUND(100.0 * SUM(wanted_on = ordered_on) / COUNT(*), 2) AS instant_pct FROM deliveries",
         "WITH firsts AS (SELECT ordered_on, wanted_on, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY ordered_on DESC, id) AS rn FROM deliveries) SELECT ROUND(100.0 * SUM(wanted_on = ordered_on) / COUNT(*), 2) AS instant_pct FROM firsts WHERE rn = 1"])

# --- JSON data --------------------------------------------------------------------------------------

PAGE_EVENTS = T("page_events", ("id", "INTEGER", "pk"), ("payload", "TEXT"))
DEVICES = ["ios", "android", "web"]


def payload_gen(rng, n, k):
    rows = []
    for i in range(n + 1):
        doc = {}
        if rng.random() < 0.85:
            doc["device"] = rng.choice(DEVICES)
        if rng.random() < 0.85:
            doc["ms"] = rng.choice([100, 200]) if ties(k) else rng.randint(40, 900)
        if rng.random() < 0.3:
            doc["page"] = rng.choice(["/", "/cart", "/help"])
        rows.append((i + 1, json.dumps(doc)))
    return {"page_events": rows}

PAYLOAD_EX = {"page_events": [(1, '{"device": "ios", "ms": 120}'), (2, '{"ms": 340, "page": "/cart"}'), (3, '{"device": "web", "ms": 95}'), (4, '{"device": "ios"}')]}

P("event-devices", "Event Devices", "json-data", "json-fields", "easy",
  """
  Each event's `payload` is a JSON object, such as `{"device": "ios", "ms": 120}`. Some payloads have no `device`.

  Return each event's `id` and `device` (NULL when the payload has none), in any order.
  """,
  [PAGE_EVENTS],
  "SELECT id, json_extract(payload, '$.device') AS device FROM page_events",
  [(PAYLOAD_EX, "Event 2's payload has no device, so it's NULL.")],
  payload_gen,
  wrong=["SELECT id, json_extract(payload, '$.Device') AS device FROM page_events",
         "SELECT id, json_extract(payload, '$.page') AS device FROM page_events"],
  notes="`json_extract(doc, '$.key')` reads a field; a missing field gives NULL. SQLite also has `doc ->> '$.key'`.")

P("load-time-by-device", "Load Time by Device", "json-data", "json-fields", "medium",
  """
  Using the same JSON payloads, find the average load time (`ms`) per device. Only count events whose payload has both
  a `device` and an `ms`.

  Return `device` and `avg_ms` (rounded to 1 decimal place), ordered by `device`.
  """,
  [PAGE_EVENTS],
  """
  SELECT json_extract(payload, '$.device') AS device,
         ROUND(AVG(json_extract(payload, '$.ms')), 1) AS avg_ms
  FROM page_events
  WHERE json_extract(payload, '$.device') IS NOT NULL
    AND json_extract(payload, '$.ms') IS NOT NULL
  GROUP BY device
  ORDER BY device
  """,
  [(PAYLOAD_EX, "iOS has one event with a time (120; event 4 has none), web has 95. Event 2 has no device.")],
  payload_gen,
  ordered=True,
  wrong=["SELECT json_extract(payload, '$.device') AS device, ROUND(AVG(json_extract(payload, '$.ms')), 1) AS avg_ms FROM page_events GROUP BY device ORDER BY device",
         "SELECT json_extract(payload, '$.device') AS device, ROUND(AVG(COALESCE(json_extract(payload, '$.ms'), 0)), 1) AS avg_ms FROM page_events WHERE json_extract(payload, '$.device') IS NOT NULL GROUP BY device ORDER BY device"])

POSTS = T("posts", ("id", "INTEGER", "pk"), ("tags", "TEXT"))
TAGS = ["sql", "python", "career", "design", "news", "tips"]


def posts_gen(rng, n, k):
    rows = []
    for i in range(n + 1):
        tags = [rng.choice(TAGS[:3] if ties(k) else TAGS) for _ in range(rng.randint(0, 4))]
        rows.append((i + 1, json.dumps(tags)))
    return {"posts": rows}

P("tag-counts", "Tag Counts", "json-data", "json-arrays", "medium",
  """
  Each post's `tags` is a JSON array of strings, like `["sql", "tips"]`. A post may list the same tag twice by mistake;
  it still counts once for that tag.

  Return `tag` and `posts` (how many posts carry it), ordered by `posts` from most to fewest, then by `tag`.
  """,
  [POSTS],
  """
  SELECT j.value AS tag, COUNT(DISTINCT p.id) AS posts
  FROM posts p, json_each(p.tags) j
  GROUP BY j.value
  ORDER BY posts DESC, tag
  """,
  [({"posts": [(1, '["sql", "tips"]'), (2, '["sql", "sql", "career"]'), (3, '[]'), (4, '["tips"]')]},
    "`sql` is on posts 1 and 2 (post 2 lists it twice, but that's one post). `tips` is on posts 1 and 4.")],
  posts_gen,
  ordered=True,
  wrong=["SELECT j.value AS tag, COUNT(*) AS posts FROM posts p, json_each(p.tags) j GROUP BY j.value ORDER BY posts DESC, tag",
         "SELECT j.value AS tag, COUNT(DISTINCT p.id) AS posts FROM posts p, json_each(p.tags) j GROUP BY j.value ORDER BY tag"],
  notes="`json_each(array)` is a table with one row per element; its `value` column holds the element.")

CARTS = T("carts", ("id", "INTEGER", "pk"), ("items", "TEXT"))


def carts_gen(rng, n, k):
    rows = []
    for i in range(n + 1):
        items = [{"sku": f"K-{rng.randint(1, 9)}", "qty": rng.randint(1, 2 if ties(k) else 5)} for _ in range(rng.randint(0, 4))]
        rows.append((i + 1, json.dumps(items)))
    return {"carts": rows}

P("cart-sizes", "Cart Sizes", "json-data", "json-arrays", "medium",
  """
  Each cart's `items` is a JSON array of objects like `{"sku": "K-7", "qty": 2}`. Some carts are empty (`[]`).

  Return every cart's `id`, `lines` (how many objects its array holds) and `units` (the sum of their `qty`), with `0` for
  empty carts. Any order.
  """,
  [CARTS],
  """
  SELECT c.id,
         COUNT(j.value) AS lines,
         COALESCE(SUM(json_extract(j.value, '$.qty')), 0) AS units
  FROM carts c
  LEFT JOIN json_each(c.items) j
  GROUP BY c.id
  """,
  [({"carts": [(1, '[{"sku": "K-7", "qty": 2}, {"sku": "K-2", "qty": 1}]'), (2, '[]'), (3, '[{"sku": "K-7", "qty": 4}]')]},
    "Cart 1 has two lines and 3 units. Cart 2 is empty but still listed, with zeros.")],
  carts_gen,
  wrong=["SELECT c.id, COUNT(j.value) AS lines, SUM(json_extract(j.value, '$.qty')) AS units FROM carts c, json_each(c.items) j GROUP BY c.id",
         "SELECT c.id, json_array_length(c.items) AS lines, json_array_length(c.items) AS units FROM carts c"],
  notes="Joining a table to `json_each(...)` drops rows whose array is empty; a `LEFT JOIN` keeps them.")

done()
