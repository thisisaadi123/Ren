"""More of the questions interviews ask most, added to existing patterns."""
import _common  # noqa: F401
from _common import only
from _examples import EMP_EX
from author import FIRST, P, T, day, done, firsts, maybe, names
from worlds import CUSTOMERS, EMPLOYEES, ORDER_ITEMS, ORDERS, PRODUCTS, shop, staff, ties

EXAM = T("exam_scores", ("student", "TEXT"), ("score", "INTEGER"))


def exam_gen(rng, n, k):
    if k % 4 == 1:
        return {"exam_scores": [(s, 70) for s in firsts(rng, n)]}
    return {"exam_scores": [(s, rng.choice([60, 70, 80, 90]) if ties(k) else rng.randint(40, 100)) for s in firsts(rng, n)]}

P("third-highest-score", "Third-highest Score", "sort-limit", "top-n", "medium",
  """
  Find the **third-highest distinct score** in `exam_scores`: equal scores count once.

  Return one row with `third_highest`, or NULL in that row if there are fewer than three different scores.
  """,
  [EXAM],
  "SELECT (SELECT DISTINCT score FROM exam_scores ORDER BY score DESC LIMIT 1 OFFSET 2) AS third_highest",
  [({"exam_scores": [("Kai", 90), ("Lena", 90), ("Mina", 85), ("Noor", 70), ("Otto", 85)]}, "The different scores are 90, 85 and 70, so the third is 70.")],
  exam_gen,
  wrong=["SELECT score AS third_highest FROM exam_scores ORDER BY score DESC LIMIT 1 OFFSET 2",
         "SELECT (SELECT DISTINCT score FROM exam_scores ORDER BY score DESC LIMIT 1 OFFSET 3) AS third_highest"])

SEATING = T("seating", ("id", "INTEGER", "pk"), ("student", "TEXT"))

P("swap-seats", "Swap Seats", "conditional", "case-when", "medium",
  """
  Seats are numbered `1, 2, 3…` with no gaps. The teacher swaps every pair of neighbours: 1 with 2, 3 with 4, and so on.
  If the count is odd, the last student stays put.

  Return `id` and `student` after the swap, ordered by `id`.
  """,
  [SEATING],
  """
  SELECT CASE WHEN id % 2 = 1 AND id = (SELECT MAX(id) FROM seating) THEN id
              WHEN id % 2 = 1 THEN id + 1
              ELSE id - 1 END AS id,
         student
  FROM seating
  ORDER BY id
  """,
  [({"seating": [(1, "Ava"), (2, "Bilal"), (3, "Chen"), (4, "Dara"), (5, "Elif")]},
    "Ava and Bilal swap, Chen and Dara swap, and Elif has no partner, so she keeps seat 5.")],
  lambda rng, n, k: {"seating": [(i + 1, s) for i, s in enumerate(firsts(rng, n + 1))]},
  ordered=True,
  wrong=["SELECT CASE WHEN id % 2 = 1 THEN id + 1 ELSE id - 1 END AS id, student FROM seating ORDER BY id",
         "SELECT id, student FROM seating ORDER BY id"])

RIDERS = T("riders", ("user_id", "INTEGER", "pk"), ("banned", "TEXT"), ("role", "TEXT"))
TRIPS = T("trips", ("id", "INTEGER", "pk"), ("client_id", "INTEGER", "fk riders.user_id"), ("driver_id", "INTEGER", "fk riders.user_id"), ("status", "TEXT"), ("requested_on", "TEXT"))


def trips_gen(rng, n, k):
    clients = [(i, "Yes" if rng.random() < 0.25 else "No", "client") for i in range(1, max(2, n // 3 + 2) + 1)]
    drivers = [(i, "Yes" if rng.random() < 0.25 else "No", "driver") for i in range(100, 100 + max(2, n // 4 + 2))]
    trips = []
    for t in range(n + 3):
        trips.append((t + 1, rng.choice(clients)[0], rng.choice(drivers)[0],
                      rng.choice(["completed", "completed", "cancelled_by_driver", "cancelled_by_client"]), day(rng.randint(0, 4), (2024, 10, 1))))
    return {"riders": clients + drivers, "trips": trips}

P("cancellation-rate-unbanned", "Cancellation Rate Without Banned Users", "conditional", "conditional-aggregation", "hard",
  """
  A trip counts only if **neither** its client nor its driver is banned (`banned = 'Yes'`). For each day from
  **2024-10-01 to 2024-10-03**, the cancellation rate is the share of counted trips whose status starts with
  `'cancelled'` (by the driver or by the client).

  Return `day` and `cancellation_rate` (a fraction between 0 and 1, rounded to 2 decimal places) for each of those days
  that has counted trips, ordered by `day`.
  """,
  [RIDERS, TRIPS],
  """
  SELECT t.requested_on AS day,
         ROUND(1.0 * SUM(CASE WHEN t.status <> 'completed' THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancellation_rate
  FROM trips t
  JOIN riders c ON c.user_id = t.client_id AND c.banned = 'No'
  JOIN riders d ON d.user_id = t.driver_id AND d.banned = 'No'
  WHERE t.requested_on BETWEEN '2024-10-01' AND '2024-10-03'
  GROUP BY t.requested_on
  ORDER BY day
  """,
  [({"riders": [(1, "No", "client"), (2, "Yes", "client"), (10, "No", "driver"), (11, "No", "driver")],
     "trips": [(1, 1, 10, "completed", "2024-10-01"), (2, 1, 11, "cancelled_by_driver", "2024-10-01"), (3, 2, 10, "cancelled_by_client", "2024-10-01"),
               (4, 1, 10, "completed", "2024-10-02"), (5, 1, 11, "completed", "2024-10-04")]},
    "On October 1, trip 3 doesn't count (client 2 is banned): 1 cancellation in 2 trips is 0.5. October 2 had none. October 4 is outside the range.")],
  trips_gen,
  ordered=True,
  wrong=["SELECT t.requested_on AS day, ROUND(1.0 * SUM(CASE WHEN t.status <> 'completed' THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancellation_rate FROM trips t WHERE t.requested_on BETWEEN '2024-10-01' AND '2024-10-03' GROUP BY t.requested_on ORDER BY day",
         "SELECT t.requested_on AS day, ROUND(1.0 * SUM(CASE WHEN t.status = 'cancelled_by_driver' THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancellation_rate FROM trips t JOIN riders c ON c.user_id = t.client_id AND c.banned = 'No' JOIN riders d ON d.user_id = t.driver_id AND d.banned = 'No' WHERE t.requested_on BETWEEN '2024-10-01' AND '2024-10-03' GROUP BY t.requested_on ORDER BY day"])

PAYMENTS = T("payments", ("id", "INTEGER", "pk"), ("country", "TEXT"), ("state", "TEXT"), ("amount", "INTEGER"), ("paid_on", "TEXT"))


def payments_gen(rng, n, k):
    return {"payments": [(i + 1, rng.choice(["DE", "IN", "US"]), rng.choice(["approved", "approved", "declined"]), rng.choice([100, 200]) if ties(k) else rng.randint(5, 900), day(rng.randint(0, 120), (2024, 1, 1))) for i in range(n + 1)]}

P("monthly-payments", "Monthly Payments", "conditional", "conditional-aggregation", "medium",
  """
  For each month (`YYYY-MM`) and `country`, return:

  - `month`, `country`
  - `payments` and `approved` (how many payments, and how many were approved)
  - `total` and `approved_total` (the amounts of all payments, and of approved ones)

  Order by `month`, then `country`.
  """,
  [PAYMENTS],
  """
  SELECT strftime('%Y-%m', paid_on) AS month, country,
         COUNT(*) AS payments,
         SUM(CASE WHEN state = 'approved' THEN 1 ELSE 0 END) AS approved,
         SUM(amount) AS total,
         SUM(CASE WHEN state = 'approved' THEN amount ELSE 0 END) AS approved_total
  FROM payments
  GROUP BY month, country
  ORDER BY month, country
  """,
  [({"payments": [(1, "US", "approved", 100, "2024-01-05"), (2, "US", "declined", 40, "2024-01-09"), (3, "DE", "approved", 70, "2024-01-20"), (4, "US", "approved", 30, "2024-02-02")]},
    "In January, the US had two payments (140 in total), one approved (100).")],
  payments_gen,
  ordered=True,
  wrong=["SELECT strftime('%Y-%m', paid_on) AS month, country, COUNT(*) AS payments, SUM(CASE WHEN state = 'approved' THEN 1 ELSE 0 END) AS approved, SUM(amount) AS total, SUM(CASE WHEN state = 'approved' THEN 1 ELSE 0 END) AS approved_total FROM payments GROUP BY month, country ORDER BY month, country",
         "SELECT strftime('%Y-%m', paid_on) AS month, country, COUNT(*) AS payments, COUNT(CASE WHEN state = 'approved' THEN 1 ELSE 0 END) AS approved, SUM(amount) AS total, SUM(CASE WHEN state = 'approved' THEN amount ELSE 0 END) AS approved_total FROM payments GROUP BY month, country ORDER BY month, country"])

NUMBERS = T("numbers", ("num", "INTEGER"))


def numbers_gen(rng, n, k):
    if k % 4 == 1:
        vals = [rng.randint(1, 5) for _ in range(n + 1)]
        return {"numbers": [(v,) for v in vals + vals]}  # every number at least twice
    return {"numbers": [(rng.randint(1, max(3, n)),) for _ in range(n + 1)]}

P("biggest-single-number", "Biggest Single Number", "aggregation", "having", "medium",
  """
  A **single number** appears exactly once in `numbers`. Return one row with `num`: the largest single number, or NULL
  if no number appears only once.
  """,
  [NUMBERS],
  "SELECT (SELECT num FROM numbers GROUP BY num HAVING COUNT(*) = 1 ORDER BY num DESC LIMIT 1) AS num",
  [({"numbers": [(8,), (8,), (3,), (3,), (1,), (4,), (5,), (6,)]}, "8 and 3 appear twice. Of the single numbers 1, 4, 5 and 6, the biggest is 6."),
   ({"numbers": [(8,), (8,), (7,), (7,)]}, "Every number appears twice, so the answer is NULL.")],
  numbers_gen,
  wrong=["SELECT MAX(DISTINCT num) AS num FROM numbers",
         "SELECT num FROM numbers GROUP BY num HAVING COUNT(*) = 1 ORDER BY num DESC LIMIT 1"])

QUEUE = T("bus_queue", ("person_id", "INTEGER", "pk"), ("name", "TEXT"), ("weight", "INTEGER"), ("turn", "INTEGER"))


def queue_gen(rng, n, k):
    turns = rng.sample(range(1, n + 3), n + 2)
    return {"bus_queue": [(i + 1, nm, rng.choice([100, 250]) if ties(k) else rng.randint(40, 400), turns[i]) for i, nm in enumerate(firsts(rng, n + 2))]}

P("last-to-board", "Last to Board", "window-aggregates", "running-totals", "medium",
  """
  People board a bus in order of `turn`. The bus holds at most **1000 kg**; boarding stops before the first person who
  would push the total over 1000.

  Return one row with `name`: the last person who gets on. (The first person always fits.)
  """,
  [QUEUE],
  """
  SELECT name FROM (
    SELECT name, turn, SUM(weight) OVER (ORDER BY turn) AS total FROM bus_queue
  )
  WHERE total <= 1000
  ORDER BY turn DESC
  LIMIT 1
  """,
  [({"bus_queue": [(5, "Alice", 250, 1), (4, "Bob", 175, 5), (3, "Alex", 350, 2), (6, "John", 400, 3), (1, "Winston", 500, 6), (2, "Marie", 200, 4)]},
    "In boarding order: Alice (250), Alex (600), John (1000), then Marie would make 1200. John is last on.")],
  queue_gen,
  wrong=["SELECT name FROM (SELECT name, turn, SUM(weight) OVER (ORDER BY turn) AS total FROM bus_queue) WHERE total < 1000 ORDER BY turn DESC LIMIT 1",
         "SELECT name FROM (SELECT name, turn, SUM(weight) OVER (ORDER BY person_id) AS total FROM bus_queue) WHERE total <= 1000 ORDER BY turn DESC LIMIT 1"])

P("new-customers-so-far", "New Customers So Far", "window-aggregates", "running-totals", "medium",
  """
  A customer is **new** on the day of their first order. For each day with orders, return `ordered_on`,
  `new_customers` (customers whose first order was that day) and `customers_so_far` (everyone who had ordered by the
  end of that day). Order by `ordered_on`.
  """,
  [ORDERS],
  """
  WITH firsts AS (
    SELECT customer_id, MIN(ordered_on) AS first_day FROM orders GROUP BY customer_id
  ),
  days AS (
    SELECT DISTINCT ordered_on FROM orders
  )
  SELECT d.ordered_on,
         COUNT(f.customer_id) AS new_customers,
         SUM(COUNT(f.customer_id)) OVER (ORDER BY d.ordered_on) AS customers_so_far
  FROM days d
  LEFT JOIN firsts f ON f.first_day = d.ordered_on
  GROUP BY d.ordered_on
  ORDER BY d.ordered_on
  """,
  [({"orders": [(1, 1, "2024-01-03", "delivered"), (2, 2, "2024-01-03", "shipped"), (3, 1, "2024-01-05", "delivered"), (4, 3, "2024-01-06", "cancelled")]},
    "Customers 1 and 2 first ordered on January 3. On January 5 only customer 1 came back, so nobody is new (still 2 so far). Customer 3 is new on the 6th.")],
  lambda rng, n, k: only(shop(rng, n * 2, k, span=max(3, n // 2)), "orders"),
  ordered=True,
  wrong=["SELECT ordered_on, COUNT(DISTINCT customer_id) AS new_customers, SUM(COUNT(DISTINCT customer_id)) OVER (ORDER BY ordered_on) AS customers_so_far FROM orders GROUP BY ordered_on ORDER BY ordered_on",
         "WITH firsts AS (SELECT customer_id, MIN(ordered_on) AS first_day FROM orders GROUP BY customer_id) SELECT first_day AS ordered_on, COUNT(*) AS new_customers, SUM(COUNT(*)) OVER (ORDER BY first_day) AS customers_so_far FROM firsts GROUP BY first_day ORDER BY ordered_on"])

STADIUM = T("stadium", ("id", "INTEGER", "pk"), ("visit_day", "TEXT"), ("people", "INTEGER"))


def stadium_gen(rng, n, k):
    vals = [rng.randint(0, 250) for _ in range(n + 4)]
    if k % 4 != 3:
        at = rng.randint(0, len(vals) - 3)
        vals[at:at + 3] = [rng.randint(100, 300) for _ in range(3)]
    return {"stadium": [(i + 1, day(i), v) for i, v in enumerate(vals)]}

P("crowded-stretches", "Crowded Stretches", "gaps-islands", "streaks", "hard",
  """
  `stadium` has one row per day, with `id` going up by one each day. A day is **crowded** if `people` is at least 100.

  Return every row that is part of a run of **three or more** consecutive crowded days: `id`, `visit_day` and `people`,
  ordered by `visit_day`.
  """,
  [STADIUM],
  """
  WITH crowded AS (
    SELECT id, visit_day, people, id - ROW_NUMBER() OVER (ORDER BY id) AS grp
    FROM stadium WHERE people >= 100
  )
  SELECT id, visit_day, people FROM crowded
  WHERE grp IN (SELECT grp FROM crowded GROUP BY grp HAVING COUNT(*) >= 3)
  ORDER BY visit_day
  """,
  [({"stadium": [(1, "2024-01-01", 10), (2, "2024-01-02", 109), (3, "2024-01-03", 150), (4, "2024-01-04", 99), (5, "2024-01-05", 145), (6, "2024-01-06", 1455), (7, "2024-01-07", 199), (8, "2024-01-08", 188)]},
    "Days 5 to 8 are four crowded days in a row. Days 2 and 3 are crowded too, but only two in a row.")],
  stadium_gen,
  ordered=True,
  wrong=["SELECT id, visit_day, people FROM (SELECT id, visit_day, people, LAG(people) OVER (ORDER BY id) AS p, LEAD(people) OVER (ORDER BY id) AS q FROM stadium) WHERE people >= 100 AND p >= 100 AND q >= 100 ORDER BY visit_day",
         "SELECT id, visit_day, people FROM stadium WHERE people >= 100 ORDER BY visit_day"])

CHECKS = T("health_checks", ("day", "TEXT", "pk"), ("ok", "INTEGER"))


def checks_gen(rng, n, k):
    state, rows = rng.randint(0, 1), []
    for i in range(n + 1):
        if rng.random() < 0.3:
            state = 1 - state
        rows.append((day(i, (2024, 3, 1)), state))
    return {"health_checks": rows}

P("up-and-down-periods", "Up and Down Periods", "gaps-islands", "streaks", "hard",
  """
  A service was checked once a day, every day; `ok` is `1` if it was up. Report the periods of consecutive days in the
  same state.

  Return `state` (`'up'` or `'down'`), `start_day` and `end_day` of each period, ordered by `start_day`.
  """,
  [CHECKS],
  """
  WITH marked AS (
    SELECT day, ok,
           ROW_NUMBER() OVER (ORDER BY day) - ROW_NUMBER() OVER (PARTITION BY ok ORDER BY day) AS grp
    FROM health_checks
  )
  SELECT CASE WHEN ok = 1 THEN 'up' ELSE 'down' END AS state, MIN(day) AS start_day, MAX(day) AS end_day
  FROM marked
  GROUP BY ok, grp
  ORDER BY start_day
  """,
  [({"health_checks": [("2024-03-01", 1), ("2024-03-02", 1), ("2024-03-03", 0), ("2024-03-04", 1), ("2024-03-05", 1), ("2024-03-06", 1)]},
    "Up for two days, down on March 3, then up again from the 4th to the 6th.")],
  checks_gen,
  ordered=True,
  wrong=["SELECT CASE WHEN ok = 1 THEN 'up' ELSE 'down' END AS state, MIN(day) AS start_day, MAX(day) AS end_day FROM health_checks GROUP BY ok ORDER BY start_day",
         "WITH marked AS (SELECT day, ok, ROW_NUMBER() OVER (ORDER BY day) - ROW_NUMBER() OVER (ORDER BY day) AS grp FROM health_checks) SELECT CASE WHEN ok = 1 THEN 'up' ELSE 'down' END AS state, MIN(day) AS start_day, MAX(day) AS end_day FROM marked GROUP BY ok, grp ORDER BY start_day"],
  notes="Two row numbers, one over all days and one within each state, drift apart by one every time the state changes, so their difference names each period.")

TREE = T("tree", ("id", "INTEGER", "pk"), ("parent_id", "INTEGER", "fk tree.id"))


def tree_gen(rng, n, k):
    return {"tree": [(i + 1, None if i == 0 else rng.randint(1, i)) for i in range(n + 1)]}

P("node-types", "Node Types", "recursive", "hierarchies", "medium",
  """
  `tree` stores a tree: the node with no `parent_id` is the **root**. A node with children is **inner**; a node with no
  children is a **leaf**. (A root alone is still the root.)

  Return `id` and `kind` (`'root'`, `'inner'` or `'leaf'`), ordered by `id`.
  """,
  [TREE],
  """
  SELECT t.id,
         CASE WHEN t.parent_id IS NULL THEN 'root'
              WHEN EXISTS (SELECT 1 FROM tree c WHERE c.parent_id = t.id) THEN 'inner'
              ELSE 'leaf' END AS kind
  FROM tree t
  ORDER BY t.id
  """,
  [({"tree": [(1, None), (2, 1), (3, 1), (4, 2), (5, 2)]}, "Node 1 is the root. Node 2 has children 4 and 5, so it's inner. Nodes 3, 4 and 5 have no children.")],
  tree_gen,
  ordered=True,
  wrong=["SELECT t.id, CASE WHEN EXISTS (SELECT 1 FROM tree c WHERE c.parent_id = t.id) THEN 'inner' WHEN t.parent_id IS NULL THEN 'root' ELSE 'leaf' END AS kind FROM tree t ORDER BY t.id",
         "SELECT t.id, CASE WHEN t.parent_id IS NULL THEN 'root' WHEN t.id IN (SELECT parent_id FROM tree) THEN 'leaf' ELSE 'inner' END AS kind FROM tree t ORDER BY t.id"])

VISITS = T("visits", ("user_id", "INTEGER"), ("visit_day", "TEXT"))
BUYS = T("buys", ("user_id", "INTEGER"), ("buy_day", "TEXT"), ("amount", "INTEGER"))


def visits_gen(rng, n, k):
    visits = sorted({(rng.randint(1, max(1, n // 3 + 1)), day(rng.randint(0, max(2, n // 2)))) for _ in range(n + 1)})
    buys = []
    for u, d in visits:
        for _ in range(rng.choice([0, 0, 1, 1, 3] if ties(k) else [0, 0, 1, 2, 3])):
            buys.append((u, d, rng.randint(5, 90)))
    return {"visits": visits, "buys": buys}

P("buys-per-visit", "Buys per Visit", "recursive", "series", "hard",
  """
  Every purchase happens during a visit: the same user, the same day (a user visits at most once a day). For each
  number of purchases from **0 up to the most made in any visit**, count how many visits had exactly that many.

  Return `buys` and `visits`, ordered by `buys`. Numbers no visit had still appear, with 0.
  """,
  [VISITS, BUYS],
  """
  WITH RECURSIVE per_visit AS (
    SELECT v.user_id, v.visit_day, COUNT(b.user_id) AS buys
    FROM visits v
    LEFT JOIN buys b ON b.user_id = v.user_id AND b.buy_day = v.visit_day
    GROUP BY v.user_id, v.visit_day
  ),
  counts(buys) AS (
    SELECT 0
    UNION ALL
    SELECT buys + 1 FROM counts WHERE buys < (SELECT MAX(buys) FROM per_visit)
  )
  SELECT c.buys, COUNT(p.user_id) AS visits
  FROM counts c
  LEFT JOIN per_visit p ON p.buys = c.buys
  GROUP BY c.buys
  ORDER BY c.buys
  """,
  [({"visits": [(1, "2024-01-01"), (2, "2024-01-01"), (1, "2024-01-02"), (3, "2024-01-02")],
     "buys": [(1, "2024-01-01", 20), (1, "2024-01-01", 5), (1, "2024-01-01", 9), (3, "2024-01-02", 40)]},
    "Two visits had no purchases, one had 1, and user 1's first visit had 3. Nobody made exactly 2, but 2 still shows, with 0.")],
  visits_gen,
  ordered=True,
  wrong=["SELECT buys, COUNT(*) AS visits FROM (SELECT v.user_id, v.visit_day, COUNT(b.user_id) AS buys FROM visits v LEFT JOIN buys b ON b.user_id = v.user_id AND b.buy_day = v.visit_day GROUP BY v.user_id, v.visit_day) GROUP BY buys ORDER BY buys",
         "SELECT buys, COUNT(*) AS visits FROM (SELECT v.user_id, v.visit_day, COUNT(*) AS buys FROM visits v LEFT JOIN buys b ON b.user_id = v.user_id AND b.buy_day = v.visit_day GROUP BY v.user_id, v.visit_day) GROUP BY buys ORDER BY buys"],
  notes="In SQLite, `WITH RECURSIVE` goes at the start and covers every CTE in the list, recursive or not.")

MAILS = T("members", ("id", "INTEGER", "pk"), ("name", "TEXT"), ("mail", "TEXT"))


def mails_gen(rng, n, k):
    rows = []
    for i, nm in enumerate(firsts(rng, n + 1)):
        user = nm.lower()
        kind = rng.randint(0, 6)
        if kind == 1:
            user = "_" + user
        elif kind == 2:
            user = user + "#1"
        elif kind == 3:
            user = user + ".x-2"
        domain = rng.choice(["@ren.example", "@ren.example", "@REN.example", "@ren.examples", "@ren-example"])
        rows.append((i + 1, nm, (user[0].upper() + user[1:] if rng.random() < 0.3 else user) + domain))
    return {"members": rows}

P("valid-emails", "Valid Emails", "strings-dates", "string-functions", "medium",
  """
  A member's `mail` is valid if:

  - the part before `@` **starts with a letter** and contains only letters, digits, `_`, `.` or `-`, and
  - the domain is exactly `@ren.example` (lowercase).

  Return `id` and `mail` of the valid ones, ordered by `id`.
  """,
  [MAILS],
  """
  SELECT id, mail FROM members
  WHERE mail GLOB '[A-Za-z]*@ren.example'
    AND substr(mail, 1, length(mail) - length('@ren.example')) NOT GLOB '*[^A-Za-z0-9_.-]*'
  ORDER BY id
  """,
  [({"members": [(1, "Kai", "kai@ren.example"), (2, "Lena", "_lena@ren.example"), (3, "Mina", "mina#1@ren.example"), (4, "Noor", "Noor.x-2@ren.example"), (5, "Otto", "otto@REN.example")]},
    "Lena's starts with `_`, Mina's has a `#`, and Otto's domain is in capitals. Kai's and Noor's are valid.")],
  mails_gen,
  ordered=True,
  wrong=["SELECT id, mail FROM members WHERE mail LIKE '%@ren.example' ORDER BY id",
         "SELECT id, mail FROM members WHERE mail GLOB '*@ren.example' AND substr(mail, 1, length(mail) - length('@ren.example')) NOT GLOB '*[^A-Za-z0-9_.-]*' ORDER BY id"],
  notes="SQLite has no regular expressions by default, but `GLOB` is case-sensitive and supports `*`, `?` and character classes like `[A-Za-z]` and `[^0-9]`. `LIKE` ignores case.")

NAMES = T("signups_raw", ("id", "INTEGER", "pk"), ("name", "TEXT"))


def raw_names_gen(rng, n, k):
    rows = []
    for i, nm in enumerate(firsts(rng, n + 1)):
        style = rng.randint(0, 3)
        rows.append((i + 1, [nm.lower(), nm.upper(), nm, nm[0].lower() + nm[1:].upper()][style]))
    return {"signups_raw": rows}

P("fix-name-case", "Fix Name Case", "strings-dates", "string-functions", "easy",
  """
  Names were typed in any case: `aVA`, `BILAL`, `chen`. Fix each so only the first letter is uppercase.

  Return `id` and `name`, ordered by `id`.
  """,
  [NAMES],
  "SELECT id, UPPER(substr(name, 1, 1)) || LOWER(substr(name, 2)) AS name FROM signups_raw ORDER BY id",
  [({"signups_raw": [(1, "aVA"), (2, "BILAL"), (3, "chen")]}, "They become `Ava`, `Bilal` and `Chen`.")],
  raw_names_gen,
  ordered=True,
  wrong=["SELECT id, UPPER(substr(name, 1, 1)) || substr(name, 2) AS name FROM signups_raw ORDER BY id",
         "SELECT id, UPPER(substr(name, 1, 1)) || LOWER(substr(name, 1)) AS name FROM signups_raw ORDER BY id"])

P("orders-per-week", "Orders per Week", "strings-dates", "date-functions", "medium",
  """
  Weeks start on **Monday**. Count orders per week, labelling each week by its Monday's date.

  Return `week_start` (`YYYY-MM-DD`) and `orders`, ordered by `week_start`. Weeks with no orders don't appear.
  """,
  [ORDERS],
  "SELECT date(ordered_on, '-6 days', 'weekday 1') AS week_start, COUNT(*) AS orders FROM orders GROUP BY week_start ORDER BY week_start",
  [({"orders": [(1, 1, "2024-01-01", "delivered"), (2, 2, "2024-01-07", "shipped"), (3, 1, "2024-01-08", "delivered"), (4, 3, "2024-01-10", "delivered")]},
    "January 1, 2024 was a Monday, and the 7th was the Sunday of that week. The 8th starts a new week.")],
  lambda rng, n, k: only(shop(rng, n * 2, k, start=(2023, 12, 18), span=60), "orders"),
  ordered=True,
  wrong=["SELECT date(ordered_on, 'weekday 1') AS week_start, COUNT(*) AS orders FROM orders GROUP BY week_start ORDER BY week_start",
         "SELECT date(ordered_on, 'weekday 0', '-6 days') AS week_start, COUNT(DISTINCT customer_id) AS orders FROM orders GROUP BY week_start ORDER BY week_start"],
  notes="`date(d, 'weekday 1')` moves forward to the next Monday (or stays on a Monday). Going back 6 days first lands on the Monday that starts `d`'s week.")

OLD = T("profiles_before", ("id", "INTEGER", "pk"), ("city", "TEXT"))
NEW = T("profiles_after", ("id", "INTEGER", "pk"), ("city", "TEXT"))


def profiles_gen(rng, n, k):
    towns = ["Lisbon", "Osaka", "Pune", None]
    before = [(i + 1, rng.choice(towns)) for i in range(n + 1)]
    after = [(i, c if rng.random() < 0.5 else rng.choice(towns)) for i, c in before]
    return {"profiles_before": before, "profiles_after": after}

P("changed-cities", "Changed Cities", "select-filter", "null-checks", "medium",
  """
  Two snapshots of the same profiles hold each person's `city`, which may be NULL (unknown). A city **changed** if the
  two values differ, counting a change from NULL to a city or from a city to NULL. NULL in both is not a change.

  Return the `id` of every profile whose city changed, ordered by `id`.
  """,
  [OLD, NEW],
  "SELECT b.id FROM profiles_before b JOIN profiles_after a ON a.id = b.id WHERE b.city IS NOT a.city ORDER BY b.id",
  [({"profiles_before": [(1, "Lisbon"), (2, None), (3, "Osaka"), (4, None)], "profiles_after": [(1, "Pune"), (2, "Osaka"), (3, None), (4, None)]},
    "Profiles 1, 2 and 3 changed (2 gained a city, 3 lost one). Profile 4 is unknown in both.")],
  profiles_gen,
  ordered=True,
  wrong=["SELECT b.id FROM profiles_before b JOIN profiles_after a ON a.id = b.id WHERE b.city <> a.city ORDER BY b.id",
         "SELECT b.id FROM profiles_before b JOIN profiles_after a ON a.id = b.id WHERE COALESCE(b.city, '') <> COALESCE(a.city, 'x') ORDER BY b.id"],
  notes="`a <> b` is NULL (not true) when either side is NULL. `a IS NOT b` treats two NULLs as equal and NULL vs a value as different.")

FREQ = T("frequencies", ("num", "INTEGER", "pk"), ("frequency", "INTEGER"))


def freq_gen(rng, n, k):
    nums = rng.sample(range(0, 50), min(50, n + 1))
    return {"frequencies": [(x, rng.randint(1, 2 if ties(k) else 9)) for x in nums]}

P("median-from-frequencies", "Median from Frequencies", "reporting", "median-percentile", "hard",
  """
  `frequencies` says how many times each `num` appears in a long list (the list itself isn't stored). Find the list's
  **median**: the middle value when sorted, or the average of the two middle values when the list's length is even.

  Return one row with `median`, rounded to 1 decimal place.
  """,
  [FREQ],
  """
  WITH running AS (
    SELECT num, frequency,
           SUM(frequency) OVER (ORDER BY num) AS upto,
           SUM(frequency) OVER () AS total
    FROM frequencies
  )
  SELECT ROUND(AVG(num), 1) AS median
  FROM running
  WHERE upto >= total / 2.0 AND upto - frequency <= total / 2.0
  """,
  [({"frequencies": [(0, 7), (1, 1), (2, 3), (3, 1)]}, "The list is seven 0s, one 1, three 2s and one 3: 12 values. The 6th and 7th are both 0, so the median is 0.0."),
   ({"frequencies": [(4, 1), (6, 2), (9, 1)]}, "The list is 4, 6, 6, 9. The middle two are 6 and 6: median 6.0.")],
  freq_gen,
  wrong=["SELECT ROUND(AVG(num), 1) AS median FROM frequencies",
         "WITH running AS (SELECT num, frequency, SUM(frequency) OVER (ORDER BY num) AS upto, SUM(frequency) OVER () AS total FROM frequencies) SELECT ROUND(AVG(num), 1) AS median FROM running WHERE upto >= total / 2 AND upto - frequency <= total / 2"],
  notes="A value covers positions `upto − frequency + 1` to `upto` of the sorted list. Keep the values that cover the middle position(s).")

CONTINENT = T("pupils", ("name", "TEXT"), ("continent", "TEXT"))


def pupils_gen(rng, n, k):
    names_ = firsts(rng, n + 1)
    return {"pupils": [(nm, rng.choice(["America", "Asia", "Europe"])) for nm in names_]}

P("pupils-by-continent", "Pupils by Continent", "reporting", "pivot", "hard",
  """
  Lay the pupils out in three columns, `america`, `asia` and `europe`: each column lists that continent's pupils in
  alphabetical order, top to bottom. Shorter columns are padded with NULL.

  Return the rows from top to bottom.
  """,
  [CONTINENT],
  """
  WITH numbered AS (
    SELECT name, continent, ROW_NUMBER() OVER (PARTITION BY continent ORDER BY name) AS rn FROM pupils
  )
  SELECT MAX(CASE WHEN continent = 'America' THEN name END) AS america,
         MAX(CASE WHEN continent = 'Asia' THEN name END) AS asia,
         MAX(CASE WHEN continent = 'Europe' THEN name END) AS europe
  FROM numbered
  GROUP BY rn
  ORDER BY rn
  """,
  [({"pupils": [("Jae", "America"), ("Pia", "Asia"), ("Abel", "Europe"), ("Ines", "America")]},
    "America has Ines and Jae (in that order), Asia has Pia, Europe has Abel: two rows, the second with NULL for Asia and Europe.")],
  pupils_gen,
  ordered=True,
  wrong=["SELECT MAX(CASE WHEN continent = 'America' THEN name END) AS america, MAX(CASE WHEN continent = 'Asia' THEN name END) AS asia, MAX(CASE WHEN continent = 'Europe' THEN name END) AS europe FROM pupils",
         "WITH numbered AS (SELECT name, continent, ROW_NUMBER() OVER (ORDER BY name) AS rn FROM pupils) SELECT MAX(CASE WHEN continent = 'America' THEN name END) AS america, MAX(CASE WHEN continent = 'Asia' THEN name END) AS asia, MAX(CASE WHEN continent = 'Europe' THEN name END) AS europe FROM numbered GROUP BY rn ORDER BY rn"])

VIEWERS = T("viewers", ("user_id", "INTEGER", "pk"), ("name", "TEXT"))
FILMS = T("films", ("film_id", "INTEGER", "pk"), ("title", "TEXT"))
RATINGS = T("ratings", ("film_id", "INTEGER", "fk films.film_id"), ("user_id", "INTEGER", "fk viewers.user_id"), ("rating", "INTEGER"), ("rated_on", "TEXT"))
TITLES = ["Avalon", "Bright Lake", "Cinder", "Dunes", "Echo Park", "Frost", "Glass House", "Harbor"]


def ratings_gen(rng, n, k):
    viewers = [(i + 1, nm) for i, nm in enumerate(firsts(rng, max(2, n // 3 + 2)))]
    films = [(i + 1, t) for i, t in enumerate(rng.sample(TITLES, min(8, max(2, n // 3 + 2))))]
    seen, ratings = set(), []
    for _ in range(n * 2 + 2):
        f, u = rng.choice(films)[0], rng.choice(viewers)[0]
        if (f, u) in seen:
            continue
        seen.add((f, u))
        ratings.append((f, u, rng.choice([3, 4]) if ties(k) else rng.randint(1, 5), day(rng.randint(0, 59), (2024, 1, 15))))
    if (films[0][0], viewers[0][0]) not in seen:  # make sure February has at least one rating
        ratings.append((films[0][0], viewers[0][0], 4, "2024-02-10"))
    return {"viewers": viewers, "films": films, "ratings": ratings}

P("top-rater-and-film", "Top Rater and Top Film", "set-ops", "union", "medium",
  """
  Return a single column `results` with exactly two rows:

  - the `name` of the viewer who rated the **most films** (ties: the alphabetically smallest name), and
  - the `title` of the film with the **highest average rating in February 2024** (ties: the alphabetically smallest
    title).

  The two rows can come in either order.
  """,
  [VIEWERS, FILMS, RATINGS],
  """
  SELECT * FROM (
    SELECT v.name AS results FROM ratings r JOIN viewers v ON v.user_id = r.user_id
    GROUP BY v.user_id, v.name ORDER BY COUNT(*) DESC, v.name LIMIT 1
  )
  UNION ALL
  SELECT * FROM (
    SELECT f.title FROM ratings r JOIN films f ON f.film_id = r.film_id
    WHERE r.rated_on BETWEEN '2024-02-01' AND '2024-02-29'
    GROUP BY f.film_id, f.title ORDER BY AVG(r.rating) DESC, f.title LIMIT 1
  )
  """,
  [({"viewers": [(1, "Kai"), (2, "Lena"), (3, "Mina")], "films": [(1, "Avalon"), (2, "Cinder")],
     "ratings": [(1, 1, 3, "2024-02-11"), (2, 1, 4, "2024-02-12"), (1, 2, 5, "2024-02-02"), (2, 2, 4, "2024-01-30"), (1, 3, 4, "2024-03-01")]},
    "Kai and Lena each rated two films; Kai comes first alphabetically. In February, Avalon averages (3 + 5) / 2 = 4 and Cinder 4 too, so Avalon wins the tie.")],
  ratings_gen,
  wrong=["SELECT * FROM (SELECT v.name AS results FROM ratings r JOIN viewers v ON v.user_id = r.user_id GROUP BY v.user_id, v.name ORDER BY COUNT(*) DESC LIMIT 1) UNION ALL SELECT * FROM (SELECT f.title FROM ratings r JOIN films f ON f.film_id = r.film_id WHERE r.rated_on BETWEEN '2024-02-01' AND '2024-02-29' GROUP BY f.film_id, f.title ORDER BY AVG(r.rating) DESC LIMIT 1)",
         "SELECT * FROM (SELECT v.name AS results FROM ratings r JOIN viewers v ON v.user_id = r.user_id GROUP BY v.user_id, v.name ORDER BY COUNT(*) DESC, v.name LIMIT 1) UNION ALL SELECT * FROM (SELECT f.title FROM ratings r JOIN films f ON f.film_id = r.film_id GROUP BY f.film_id, f.title ORDER BY AVG(r.rating) DESC, f.title LIMIT 1)"],
  notes="In SQLite, a `SELECT` with its own `ORDER BY` and `LIMIT` must be wrapped in a subquery before it can be part of a `UNION`.")


def left_gen(rng, n, k):
    rows = only(staff(rng, n + 2, k), "employees")["employees"]
    managers = sorted({r[3] for r in rows if r[3] is not None})
    gone = set(rng.sample(managers, max(1, len(managers) // 3))) if managers else set()
    return {"employees": [r for r in rows if r[0] not in gone]}

P("manager-left", "Manager Left", "joins", "anti-join", "easy",
  """
  Some managers have left the company: their rows are gone, but their reports still point to them in `manager_id`.

  Return the `id` and `name` of every employee whose manager is no longer in `employees`, ordered by `id`. People with no
  manager at all aren't included.
  """,
  [EMPLOYEES],
  """
  SELECT e.id, e.name FROM employees e
  LEFT JOIN employees m ON m.id = e.manager_id
  WHERE e.manager_id IS NOT NULL AND m.id IS NULL
  ORDER BY e.id
  """,
  [({"employees": [r for r in EMP_EX["employees"] if r[0] != 2]}, "Bilal (id 2) has left, so Dara and Elif, who reported to him, are listed. Ava has no manager.")],
  left_gen,
  ordered=True,
  wrong=["SELECT e.id, e.name FROM employees e LEFT JOIN employees m ON m.id = e.manager_id WHERE m.id IS NULL ORDER BY e.id",
         "SELECT e.id, e.name FROM employees e WHERE e.manager_id NOT IN (SELECT manager_id FROM employees WHERE manager_id IS NOT NULL) ORDER BY e.id"])

INCOMES = T("incomes", ("account_id", "INTEGER", "pk"), ("income", "INTEGER"))


def incomes_gen(rng, n, k):
    if k % 4 == 1:
        return {"incomes": [(i + 1, rng.randint(60000, 90000)) for i in range(n + 1)]}
    return {"incomes": [(i + 1, rng.choice([19999, 20000, 50000, 50001]) if ties(k) else rng.randint(1000, 90000)) for i in range(n + 1)]}

P("salary-categories", "Salary Categories", "joins", "cross-join", "easy",
  """
  Sort accounts into three categories by `income`:

  - `'Low Salary'`: under 20,000
  - `'Average Salary'`: 20,000 to 50,000, both included
  - `'High Salary'`: over 50,000

  Return `category` and `accounts` (how many fall in it) for **all three** categories, even if a count is 0. Any order.
  """,
  [INCOMES],
  """
  WITH categories(category) AS (VALUES ('Low Salary'), ('Average Salary'), ('High Salary')),
  labelled AS (
    SELECT CASE WHEN income < 20000 THEN 'Low Salary'
                WHEN income <= 50000 THEN 'Average Salary'
                ELSE 'High Salary' END AS category
    FROM incomes
  )
  SELECT c.category, COUNT(l.category) AS accounts
  FROM categories c LEFT JOIN labelled l ON l.category = c.category
  GROUP BY c.category
  """,
  [({"incomes": [(3, 108939), (2, 12747), (8, 87709), (6, 91796)]}, "One low salary, three high ones, and no average ones, which still shows with 0.")],
  incomes_gen,
  wrong=["SELECT CASE WHEN income < 20000 THEN 'Low Salary' WHEN income <= 50000 THEN 'Average Salary' ELSE 'High Salary' END AS category, COUNT(*) AS accounts FROM incomes GROUP BY category",
         "WITH categories(category) AS (VALUES ('Low Salary'), ('Average Salary'), ('High Salary')), labelled AS (SELECT CASE WHEN income < 20000 THEN 'Low Salary' WHEN income < 50000 THEN 'Average Salary' ELSE 'High Salary' END AS category FROM incomes) SELECT c.category, COUNT(l.category) AS accounts FROM categories c LEFT JOIN labelled l ON l.category = c.category GROUP BY c.category"])


def rising_gen(rng, n, k):
    return shop(rng, n * 3, k, start=(2024, 1, 1), span=150)

P("rising-spenders", "Rising Spenders", "ctes", "step-ctes", "hard",
  """
  A customer's monthly spend is the sum of `quantity × price` over their **delivered** orders placed that month
  (`YYYY-MM`). A **rising spender** has spend in **at least two** months, and every one of those months beats the
  previous month they spent in.

  Return the `name` of every rising spender, ordered by `name`.
  """,
  [CUSTOMERS, PRODUCTS, ORDERS, ORDER_ITEMS],
  """
  WITH monthly AS (
    SELECT o.customer_id, strftime('%Y-%m', o.ordered_on) AS month, SUM(i.quantity * p.price) AS spend
    FROM orders o
    JOIN order_items i ON i.order_id = o.id
    JOIN products p ON p.id = i.product_id
    WHERE o.status = 'delivered'
    GROUP BY o.customer_id, month
  ),
  compared AS (
    SELECT customer_id, spend, LAG(spend) OVER (PARTITION BY customer_id ORDER BY month) AS prev
    FROM monthly
  )
  SELECT c.name
  FROM compared x
  JOIN customers c ON c.id = x.customer_id
  GROUP BY x.customer_id, c.name
  HAVING COUNT(*) >= 2 AND SUM(CASE WHEN x.prev IS NOT NULL AND x.spend <= x.prev THEN 1 ELSE 0 END) = 0
  ORDER BY c.name
  """,
  [({"customers": [(1, "Omar Fox", "Osaka", "2023-02-01"), (2, "Priya Nair", "Lisbon", "2023-05-12")],
     "products": [(1, "Kettle", "Kitchen", 10.0)],
     "orders": [(1, 1, "2024-01-05", "delivered"), (2, 1, "2024-03-02", "delivered"), (3, 2, "2024-01-09", "delivered"), (4, 2, "2024-02-01", "delivered")],
     "order_items": [(1, 1, 1), (2, 1, 3), (3, 1, 2), (4, 1, 2)]},
    "Omar spent 10 in January and 30 in March: rising. Priya spent 20 in January and 20 in February, which doesn't beat the month before.")],
  rising_gen,
  ordered=True,
  wrong=["WITH monthly AS (SELECT o.customer_id, strftime('%Y-%m', o.ordered_on) AS month, SUM(i.quantity * p.price) AS spend FROM orders o JOIN order_items i ON i.order_id = o.id JOIN products p ON p.id = i.product_id WHERE o.status = 'delivered' GROUP BY o.customer_id, month), compared AS (SELECT customer_id, spend, LAG(spend) OVER (PARTITION BY customer_id ORDER BY month) AS prev FROM monthly) SELECT c.name FROM compared x JOIN customers c ON c.id = x.customer_id GROUP BY x.customer_id, c.name HAVING SUM(CASE WHEN x.prev IS NOT NULL AND x.spend <= x.prev THEN 1 ELSE 0 END) = 0 ORDER BY c.name",
         "WITH monthly AS (SELECT o.customer_id, strftime('%Y-%m', o.ordered_on) AS month, SUM(i.quantity * p.price) AS spend FROM orders o JOIN order_items i ON i.order_id = o.id JOIN products p ON p.id = i.product_id WHERE o.status = 'delivered' GROUP BY o.customer_id, month), compared AS (SELECT customer_id, spend, LAG(spend) OVER (PARTITION BY customer_id ORDER BY month) AS prev FROM monthly) SELECT c.name FROM compared x JOIN customers c ON c.id = x.customer_id GROUP BY x.customer_id, c.name HAVING COUNT(*) >= 2 AND SUM(CASE WHEN x.prev IS NOT NULL AND x.spend < x.prev THEN 1 ELSE 0 END) = 0 ORDER BY c.name"])

DAILY = T("daily_sales", ("day", "TEXT", "pk"), ("revenue", "INTEGER"))

P("calendar-week-average", "Calendar-week Average", "window-aggregates", "moving-windows", "hard",
  """
  `daily_sales` **skips** days with no data. For each recorded day, average the revenue of the recorded days in the
  **7 calendar days** ending on it (that day and the 6 before), however many of them were recorded.

  Return `day` and `avg_7d` (rounded to 2 decimal places), ordered by `day`.
  """,
  [DAILY],
  """
  SELECT day,
         ROUND(AVG(revenue) OVER (ORDER BY julianday(day) RANGE BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS avg_7d
  FROM daily_sales
  ORDER BY day
  """,
  [({"daily_sales": [("2024-05-01", 10), ("2024-05-03", 20), ("2024-05-07", 60), ("2024-05-08", 30)]},
    "May 7's window is May 1–7: 10, 20 and 60 average 30. May 8's window is May 2–8, which drops May 1: (20 + 60 + 30) / 3 = 36.67.")],
  lambda rng, n, k: {"daily_sales": [(day(d, (2024, 5, 1)), rng.randint(0, 300)) for d in sorted(rng.sample(range(0, 3 * n + 10), n + 2))]},
  ordered=True,
  wrong=["SELECT day, ROUND(AVG(revenue) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS avg_7d FROM daily_sales ORDER BY day",
         "SELECT day, ROUND(AVG(revenue) OVER (ORDER BY julianday(day) RANGE BETWEEN 7 PRECEDING AND CURRENT ROW), 2) AS avg_7d FROM daily_sales ORDER BY day"],
  notes="`ROWS` counts rows; `RANGE` with a number compares the `ORDER BY` values, here day numbers from `julianday()`, so missing days are handled.")

done()
