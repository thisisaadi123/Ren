"""Advanced: window functions for ranking and for running values."""
import _common  # noqa: F401
from _common import only
from author import FIRST, P, T, day, done, firsts, names
from worlds import DEPARTMENTS, EMPLOYEES, ORDER_ITEMS, ORDERS, PRODUCTS, USERS, app, shop, staff, ties

EMP_EX = {"employees": [
    (1, "Ava Moss", 1, None, 96000, "2019-03-04"),
    (2, "Bilal Cruz", 2, 1, 61000, "2020-07-15"),
    (3, "Chen Ito", 1, 1, 60000, "2021-01-10"),
    (4, "Dara Kerr", None, 2, 125500, "2019-03-04"),
    (5, "Elif Park", 2, 2, 48000, "2022-11-30"),
]}
LATEST_EX = {"orders": [(1, 1, "2024-01-03", "delivered"), (2, 2, "2024-01-03", "shipped"), (3, 1, "2024-01-05", "delivered"),
                        (4, 3, "2024-01-06", "cancelled"), (5, 2, "2024-01-09", "delivered"), (6, 2, "2024-01-09", "shipped")]}
SHOP_EX = {
    "products": [(1, "Kettle", "Kitchen", 24.5), (2, "Novel", "Books", 12.0), (3, "Kite", "Toys", 8.0), (4, "Comic", "Books", 6.5)],
    "orders": [(1, 1, "2024-01-03", "delivered"), (2, 2, "2024-01-04", "cancelled"),
               (3, 1, "2024-02-10", "delivered"), (4, 3, "2024-02-11", "shipped")],
    "order_items": [(1, 1, 2), (1, 2, 1), (2, 3, 3), (3, 4, 2), (4, 2, 1), (4, 3, 1)],
}

# --- Ranking -------------------------------------------------------------------------------------

P("latest-order", "Each Customer's Latest Order", "ranking", "row-number", "medium",
  """
  For every customer who has ordered, find their **most recent** order. If a customer placed several orders on their
  latest day, take the one with the highest `id`.

  Return `customer_id`, `order_id` and `ordered_on`, in any order.
  """,
  [ORDERS],
  """
  SELECT customer_id, order_id, ordered_on
  FROM (
    SELECT customer_id, id AS order_id, ordered_on,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY ordered_on DESC, id DESC) AS rn
    FROM orders
  )
  WHERE rn = 1
  """,
  [(LATEST_EX, "Customer 2 ordered twice on 2024-01-09; order 6 has the higher id, so it wins over order 5.")],
  lambda rng, n, k: only(shop(rng, n * 2, k, span=max(2, n // 3)), "orders"),
  wrong=["SELECT customer_id, order_id, ordered_on FROM (SELECT customer_id, id AS order_id, ordered_on, RANK() OVER (PARTITION BY customer_id ORDER BY ordered_on DESC) AS rn FROM orders) WHERE rn = 1",
         "SELECT customer_id, order_id, ordered_on FROM (SELECT customer_id, id AS order_id, ordered_on, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY ordered_on, id) AS rn FROM orders) WHERE rn = 1"])

P("hire-order", "Who Joined First", "ranking", "row-number", "easy",
  """
  Number the people in each department in the order they were hired: the earliest hire is `1`. People hired on the
  same day are numbered by `id`.

  Return `dept_id`, `name` and `nth` for every employee with a department, ordered by `dept_id`, then `nth`.
  """,
  [EMPLOYEES],
  """
  SELECT dept_id, name, ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY hired_on, id) AS nth
  FROM employees
  WHERE dept_id IS NOT NULL
  ORDER BY dept_id, nth
  """,
  [(EMP_EX, "In department 1, Ava (2019) joined before Chen (2021). Dara has no department.")],
  lambda rng, n, k: only(staff(rng, n, k), "employees"),
  ordered=True,
  wrong=["SELECT dept_id, name, ROW_NUMBER() OVER (ORDER BY hired_on, id) AS nth FROM employees WHERE dept_id IS NOT NULL ORDER BY dept_id, nth",
         "SELECT dept_id, name, ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY hired_on DESC, id) AS nth FROM employees WHERE dept_id IS NOT NULL ORDER BY dept_id, nth"])

SCORES = T("scores", ("player", "TEXT"), ("points", "INTEGER"))


def scores_gen(rng, n, k):
    return {"scores": [(p, rng.choice([70, 80, 90]) if k % 2 == 0 else rng.randint(0, 100)) for p in firsts(rng, n)]}

P("leaderboard", "Leaderboard", "ranking", "rank-dense", "medium",
  """
  Rank players by `points`, highest first. Players with equal points share a rank, and the next rank follows on
  without a gap (90, 90, 85 are ranks 1, 1, 2).

  Return `player`, `points` and `rank`, ordered by `rank`, then `player`.
  """,
  [SCORES],
  "SELECT player, points, DENSE_RANK() OVER (ORDER BY points DESC) AS rank FROM scores ORDER BY rank, player",
  [({"scores": [("Kai", 90), ("Lena", 85), ("Mina", 90), ("Noor", 70), ("Otto", 85)]},
    "Kai and Mina share first place. Lena and Otto are next, at rank 2, and Noor is third.")],
  scores_gen,
  ordered=True,
  wrong=["SELECT player, points, RANK() OVER (ORDER BY points DESC) AS rank FROM scores ORDER BY rank, player",
         "SELECT player, points, ROW_NUMBER() OVER (ORDER BY points DESC, player) AS rank FROM scores ORDER BY rank, player"])

RESULTS = T("results", ("event", "TEXT"), ("athlete", "TEXT"), ("seconds", "REAL"))


def results_gen(rng, n, k):
    rows = []
    events = ["100m", "200m", "400m", "800m"][: max(1, min(4, n // 3 + 1))]
    for ev in events:
        base = {"100m": 10.5, "200m": 21.5, "400m": 47.0, "800m": 105.0}[ev]
        for a in firsts(rng, max(1, n // len(events) + 1)):
            rows.append((ev, a, round(base + rng.choice([0.2, 0.4]) if ties(k) else base + rng.random() * 2, 1)))
    return {"results": rows}

P("race-placings", "Race Placings", "ranking", "rank-dense", "medium",
  """
  In each event, the fastest time (fewest `seconds`) places first. Athletes with the same time share a place, and the
  next place skips ahead (two athletes tied for 2nd means the next one is 4th).

  Return `event`, `athlete` and `place`, ordered by `event`, then `place`, then `athlete`.
  """,
  [RESULTS],
  "SELECT event, athlete, RANK() OVER (PARTITION BY event ORDER BY seconds) AS place FROM results ORDER BY event, place, athlete",
  [({"results": [("100m", "Ava", 11.2), ("100m", "Bea", 10.9), ("100m", "Cyrus", 11.2), ("100m", "Dev", 11.5), ("200m", "Emil", 22.4), ("200m", "Finn", 22.1)]},
    "In the 100m, Bea wins, Ava and Cyrus tie for 2nd, so Dev is 4th.")],
  results_gen,
  ordered=True,
  wrong=["SELECT event, athlete, DENSE_RANK() OVER (PARTITION BY event ORDER BY seconds) AS place FROM results ORDER BY event, place, athlete",
         "SELECT event, athlete, RANK() OVER (ORDER BY seconds) AS place FROM results ORDER BY event, place, athlete"])

TOP2_EX = {
    "departments": [(1, "Design", "Lisbon"), (2, "Sales", "Osaka")],
    "employees": [(1, "Ava Moss", 1, None, 96000, "2019-03-04"), (2, "Bilal Cruz", 2, 1, 61000, "2020-07-15"),
                  (3, "Chen Ito", 1, 1, 60000, "2021-01-10"), (4, "Gus Holt", 1, 1, 96000, "2021-05-02"),
                  (5, "Elif Park", 2, 2, 48000, "2022-11-30"), (6, "Hana Lund", 1, 3, 52000, "2023-03-09")],
}

P("top-two-salaries", "Top Two Salaries per Department", "ranking", "top-per-group", "medium",
  """
  In each department, find the **two highest distinct salaries**, and list everyone who earns one of them.

  Return the `department` name, the employee's `name` and `salary`, ordered by `department`, then `salary` from high to
  low, then `name`. Employees without a department are left out.
  """,
  [DEPARTMENTS, EMPLOYEES],
  """
  SELECT department, name, salary
  FROM (
    SELECT d.name AS department, e.name, e.salary,
           DENSE_RANK() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC) AS r
    FROM employees e
    JOIN departments d ON d.id = e.dept_id
  )
  WHERE r <= 2
  ORDER BY department, salary DESC, name
  """,
  [(TOP2_EX, "Design's two highest salaries are 96,000 (Ava and Gus) and 60,000 (Chen); Hana's 52,000 is third. Sales has only two people.")],
  lambda rng, n, k: staff(rng, n, k),
  ordered=True,
  wrong=["SELECT department, name, salary FROM (SELECT d.name AS department, e.name, e.salary, ROW_NUMBER() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC) AS r FROM employees e JOIN departments d ON d.id = e.dept_id) WHERE r <= 2 ORDER BY department, salary DESC, name",
         "SELECT department, name, salary FROM (SELECT d.name AS department, e.name, e.salary, RANK() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC) AS r FROM employees e JOIN departments d ON d.id = e.dept_id) WHERE r <= 2 ORDER BY department, salary DESC, name"])

P("category-bestsellers", "Bestseller in Each Category", "ranking", "top-per-group", "hard",
  """
  A product's `units` sold is the total `quantity` across all orders that weren't cancelled. In each category, find the
  product with the most units. If several products tie for the most, list them all. Products that never sold don't
  count.

  Return `category`, the product's `name` and `units`, ordered by `category`, then `name`.
  """,
  [PRODUCTS, ORDERS, ORDER_ITEMS],
  """
  WITH sold AS (
    SELECT p.id, p.category, p.name, SUM(i.quantity) AS units
    FROM order_items i
    JOIN orders o ON o.id = i.order_id
    JOIN products p ON p.id = i.product_id
    WHERE o.status <> 'cancelled'
    GROUP BY p.id, p.category, p.name
  ),
  ranked AS (
    SELECT category, name, units, RANK() OVER (PARTITION BY category ORDER BY units DESC) AS r
    FROM sold
  )
  SELECT category, name, units FROM ranked WHERE r = 1 ORDER BY category, name
  """,
  [(SHOP_EX, "Three Kites were in a cancelled order, so Kites sold only 1. In Books, the Novel and the Comic tie at 2 units each.")],
  lambda rng, n, k: only(shop(rng, n, k), "products", "orders", "order_items"),
  ordered=True,
  wrong=["WITH sold AS (SELECT p.id, p.category, p.name, SUM(i.quantity) AS units FROM order_items i JOIN products p ON p.id = i.product_id GROUP BY p.id, p.category, p.name), ranked AS (SELECT category, name, units, RANK() OVER (PARTITION BY category ORDER BY units DESC) AS r FROM sold) SELECT category, name, units FROM ranked WHERE r = 1 ORDER BY category, name",
         "WITH sold AS (SELECT p.id, p.category, p.name, SUM(i.quantity) AS units FROM order_items i JOIN orders o ON o.id = i.order_id JOIN products p ON p.id = i.product_id WHERE o.status <> 'cancelled' GROUP BY p.id, p.category, p.name), ranked AS (SELECT category, name, units, ROW_NUMBER() OVER (PARTITION BY category ORDER BY units DESC) AS r FROM sold) SELECT category, name, units FROM ranked WHERE r = 1 ORDER BY category, name"])

# --- Running values ------------------------------------------------------------------------------

TRANSACTIONS = T("transactions", ("id", "INTEGER", "pk"), ("account_id", "INTEGER"), ("made_on", "TEXT"), ("amount", "INTEGER"))


def tx_gen(rng, n, k):
    accounts = max(1, n // 4 + 1)
    rows = [(i + 1, rng.randint(1, accounts), day(rng.randint(0, 2 if ties(k) else 30)), rng.choice([-50, 20, 100]) if ties(k) else rng.randint(-200, 300)) for i in range(n)]
    rng.shuffle(rows)
    return {"transactions": rows}

P("running-balance", "Running Balance", "window-aggregates", "running-totals", "medium",
  """
  Show each account's balance after every transaction. Transactions apply in date order; on the same day, in `id`
  order. Every account starts at 0.

  Return `id`, `account_id`, `made_on` and `balance` (the account's total after this transaction), ordered by
  `account_id`, then `made_on`, then `id`.
  """,
  [TRANSACTIONS],
  """
  SELECT id, account_id, made_on,
         SUM(amount) OVER (PARTITION BY account_id ORDER BY made_on, id) AS balance
  FROM transactions
  ORDER BY account_id, made_on, id
  """,
  [({"transactions": [(1, 1, "2024-01-01", 100), (2, 2, "2024-01-01", 50), (3, 1, "2024-01-02", -30), (4, 1, "2024-01-02", 20), (5, 2, "2024-01-03", -10)]},
    "Account 1 goes 100, then 70, then 90: its two transactions on January 2 apply one at a time.")],
  tx_gen,
  ordered=True,
  wrong=["SELECT id, account_id, made_on, SUM(amount) OVER (PARTITION BY account_id ORDER BY made_on) AS balance FROM transactions ORDER BY account_id, made_on, id",
         "SELECT id, account_id, made_on, SUM(amount) OVER (ORDER BY made_on, id) AS balance FROM transactions ORDER BY account_id, made_on, id"],
  notes="With `ORDER BY made_on` alone, the window includes every row with the same date (the default frame is `RANGE`), so same-day transactions would all show the day's final balance.")

P("cumulative-signups", "Signups So Far", "window-aggregates", "running-totals", "easy",
  """
  For each day that had signups, show how many people signed up that day and how many had signed up in total by the
  end of it.

  Return `day`, `signups` and `total`, ordered by `day`.
  """,
  [USERS],
  "SELECT signed_up AS day, COUNT(*) AS signups, SUM(COUNT(*)) OVER (ORDER BY signed_up) AS total FROM users GROUP BY signed_up ORDER BY day",
  [({"users": [(1, "Ava Moss", "BR", "2024-01-01"), (2, "Bilal Cruz", "CA", "2024-01-01"), (3, "Chen Ito", "BR", "2024-01-03"),
               (4, "Dara Kerr", "DE", "2024-01-04"), (5, "Elif Park", "IN", "2024-01-04")]},
    "Two people joined on January 1, one on the 3rd (3 in total) and two on the 4th (5 in total).")],
  lambda rng, n, k: {"users": [(i + 1, nm, "BR", day(rng.randint(0, max(1, n // 3)))) for i, nm in enumerate(names(rng, n))]},
  ordered=True,
  wrong=["SELECT signed_up AS day, COUNT(*) AS signups, COUNT(*) OVER () AS total FROM users GROUP BY signed_up ORDER BY day",
         "SELECT signed_up AS day, COUNT(*) AS signups, ROW_NUMBER() OVER (ORDER BY signed_up) AS total FROM users GROUP BY signed_up ORDER BY day"],
  notes="Window functions run after `GROUP BY`, so `SUM(COUNT(*)) OVER (…)` adds up the per-day counts.")

DAILY = T("daily_sales", ("day", "TEXT", "pk"), ("revenue", "INTEGER"))


def daily_gen(rng, n, k):
    start = rng.randint(0, 200)
    return {"daily_sales": [(day(start + i), rng.choice([0, 100]) if ties(k) else rng.randint(0, 500)) for i in range(n)]}

DAILY_EX = {"daily_sales": [("2024-03-01", 10), ("2024-03-02", 20), ("2024-03-03", 60), ("2024-03-04", 30), ("2024-03-05", 0)]}

P("three-day-average", "Three-day Average", "window-aggregates", "moving-windows", "medium",
  """
  `daily_sales` has one row for every day, with no gaps. Smooth the numbers with a **3-day average**: each day's
  revenue averaged with the two days before it. The first two days average over the days available.

  Return `day` and `avg_3d`, rounded to 2 decimal places, ordered by `day`.
  """,
  [DAILY],
  "SELECT day, ROUND(AVG(revenue) OVER (ORDER BY day ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS avg_3d FROM daily_sales ORDER BY day",
  [(DAILY_EX, "March 4 averages 20, 60 and 30: 36.67. March 2 only has two days to average: 15.")],
  daily_gen,
  ordered=True,
  wrong=["SELECT day, ROUND(AVG(revenue) OVER (ORDER BY day ROWS BETWEEN 3 PRECEDING AND CURRENT ROW), 2) AS avg_3d FROM daily_sales ORDER BY day",
         "SELECT day, ROUND(AVG(revenue) OVER (ORDER BY day ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING), 2) AS avg_3d FROM daily_sales ORDER BY day"])

P("day-over-day", "Day-over-day Change", "window-aggregates", "lag-lead", "easy",
  """
  For each day in `daily_sales` (one row per day, no gaps), show how much revenue changed from the day before.

  Return `day`, `revenue` and `change` (today minus yesterday; NULL on the first day), ordered by `day`.
  """,
  [DAILY],
  "SELECT day, revenue, revenue - LAG(revenue) OVER (ORDER BY day) AS change FROM daily_sales ORDER BY day",
  [(DAILY_EX, "March 3 made 60, up 40 from March 2's 20. The first day has nothing to compare with.")],
  daily_gen,
  ordered=True,
  wrong=["SELECT day, revenue, LEAD(revenue) OVER (ORDER BY day) - revenue AS change FROM daily_sales ORDER BY day",
         "SELECT day, revenue, revenue - COALESCE(LAG(revenue) OVER (ORDER BY day), 0) AS change FROM daily_sales ORDER BY day"])

READINGS = T("readings", ("day", "TEXT", "pk"), ("temp", "INTEGER"))


def readings_gen(rng, n, k):
    rows, d = [], rng.randint(0, 100)
    for _ in range(n + 1):
        rows.append((day(d), rng.randint(0, 3) if ties(k) else rng.randint(-5, 30)))
        d += 1 if rng.random() < 0.7 else rng.randint(2, 4)
    return {"readings": rows}

P("warmer-than-yesterday", "Warmer Than Yesterday", "window-aggregates", "lag-lead", "medium",
  """
  A weather log has one `temp` per day, but some days are missing. Find the days that were **warmer than the day
  before**. If the day before wasn't logged, the day doesn't count.

  Return `day`, ordered by `day`.
  """,
  [READINGS],
  "SELECT t.day FROM readings t JOIN readings y ON y.day = date(t.day, '-1 day') WHERE t.temp > y.temp ORDER BY t.day",
  [({"readings": [("2024-01-01", 5), ("2024-01-02", 7), ("2024-01-04", 9), ("2024-01-05", 8), ("2024-01-06", 10)]},
    "January 2 beats January 1, and January 6 beats January 5. January 4 is warmer than the previous row, but the previous row is January 2, not the day before.")],
  readings_gen,
  ordered=True,
  wrong=["SELECT day FROM (SELECT day, temp, LAG(temp) OVER (ORDER BY day) AS prev FROM readings) WHERE temp > prev ORDER BY day",
         "SELECT t.day FROM readings t JOIN readings y ON y.day = date(t.day, '-1 day') WHERE t.temp >= y.temp ORDER BY t.day"],
  notes="`date('2024-01-04', '-1 day')` gives `'2024-01-03'`.")

P("days-to-next-order", "Days Until the Next Order", "window-aggregates", "lag-lead", "medium",
  """
  For every order, find how many days passed until the **same customer's next order** (by `ordered_on`, then `id`).
  A customer's last order has no next one: NULL.

  Return `customer_id`, `order_id` and `days_to_next`, ordered by `customer_id`, then `ordered_on`, then `order_id`.
  """,
  [ORDERS],
  """
  SELECT customer_id, id AS order_id,
         julianday(LEAD(ordered_on) OVER (PARTITION BY customer_id ORDER BY ordered_on, id)) - julianday(ordered_on) AS days_to_next
  FROM orders
  ORDER BY customer_id, ordered_on, order_id
  """,
  [(LATEST_EX, "Customer 2 ordered on January 3, then twice on January 9: 6 days, then 0, then no next order.")],
  lambda rng, n, k: only(shop(rng, n * 2, k, span=max(4, n)), "orders"),
  ordered=True,
  wrong=["SELECT customer_id, id AS order_id, julianday(LEAD(ordered_on) OVER (ORDER BY ordered_on, id)) - julianday(ordered_on) AS days_to_next FROM orders ORDER BY customer_id, ordered_on, order_id",
         "SELECT customer_id, id AS order_id, julianday(ordered_on) - julianday(LAG(ordered_on) OVER (PARTITION BY customer_id ORDER BY ordered_on, id)) AS days_to_next FROM orders ORDER BY customer_id, ordered_on, order_id"])

SALES = T("sales", ("region", "TEXT"), ("rep", "TEXT"), ("amount", "INTEGER"))


def sales_gen(rng, n, k):
    rows = []
    regions = ["North", "South", "East", "West"][: max(1, min(4, n // 3 + 1))]
    for r in regions:
        for rep in firsts(rng, max(1, n // len(regions) + 1)):
            rows.append((r, rep, rng.choice([100, 200]) if ties(k) else rng.randint(1, 999)))
    return {"sales": rows}

P("share-of-region", "Share of the Region", "window-aggregates", "share-of-total", "medium",
  """
  Each rep sells in one region. Show what percentage of their region's sales each rep brought in.

  Return `region`, `rep`, `amount` and `share`: the rep's amount as a percentage of the region's total, rounded to 1
  decimal place. Any order.
  """,
  [SALES],
  "SELECT region, rep, amount, ROUND(100.0 * amount / SUM(amount) OVER (PARTITION BY region), 1) AS share FROM sales",
  [({"sales": [("North", "Ava", 300), ("North", "Bilal", 100), ("South", "Chen", 200)]},
    "North sold 400 in total, so Ava's 300 is 75.0% and Bilal's 100 is 25.0%. Chen is South's only rep: 100.0%.")],
  sales_gen,
  wrong=["SELECT region, rep, amount, ROUND(100 * amount / SUM(amount) OVER (PARTITION BY region), 1) AS share FROM sales",
         "SELECT region, rep, amount, ROUND(100.0 * amount / SUM(amount) OVER (), 1) AS share FROM sales"])

done()
