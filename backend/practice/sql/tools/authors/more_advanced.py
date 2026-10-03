"""Filling the Advanced topics up to their planned counts."""
import _common  # noqa: F401
from _common import only
from _examples import EMP_EX, LATEST_EX, SCHOOL_EX, SHOP_EX
from author import P, T, day, done
from worlds import COURSES, CUSTOMERS, EMPLOYEES, ENROLLMENTS, ORDER_ITEMS, ORDERS, PRODUCTS, STUDENTS, app, school, shop, staff, ties

ex = lambda data, *tables: only(data, *tables)  # noqa: E731

P("second-order", "Each Customer's Second Order", "ranking", "row-number", "medium",
  """
  For every customer with at least two orders, find their **second** order, counting from the earliest (by
  `ordered_on`, then `id`).

  Return `customer_id`, `order_id` and `ordered_on`, in any order.
  """,
  [ORDERS],
  """
  SELECT customer_id, order_id, ordered_on
  FROM (
    SELECT customer_id, id AS order_id, ordered_on,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY ordered_on, id) AS rn
    FROM orders
  )
  WHERE rn = 2
  """,
  [(LATEST_EX, "Customer 1's orders are 1 then 3, so the second is 3. Customer 2's are 2, 5 and 6 (5 and 6 on the same day, 5 first by id). Customer 3 ordered only once.")],
  lambda rng, n, k: only(shop(rng, n * 2, k, span=max(2, n // 3)), "orders"),
  wrong=["SELECT customer_id, order_id, ordered_on FROM (SELECT customer_id, id AS order_id, ordered_on, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY ordered_on DESC, id DESC) AS rn FROM orders) WHERE rn = 2",
         "SELECT customer_id, order_id, ordered_on FROM (SELECT customer_id, id AS order_id, ordered_on, DENSE_RANK() OVER (PARTITION BY customer_id ORDER BY ordered_on) AS rn FROM orders) WHERE rn = 2"])

P("salary-percentile", "Salary Percentile", "ranking", "rank-dense", "medium",
  """
  An employee's **percentile** is the share of the *other* employees who earn strictly less, as a percentage: the
  lowest earner is at 0 and the highest at 100. People with equal salaries share a percentile; a company of one person
  puts them at 0.

  Return `name`, `salary` and `percentile`, rounded to 1 decimal place, in any order.
  """,
  [EMPLOYEES],
  "SELECT name, salary, ROUND(100 * PERCENT_RANK() OVER (ORDER BY salary), 1) AS percentile FROM employees",
  [(EMP_EX, "With five people, every colleague you out-earn adds 25. Bilal out-earns Elif and Chen, so he is at 50.0; Dara out-earns everyone: 100.0.")],
  lambda rng, n, k: only(staff(rng, n, k), "employees"),
  wrong=["SELECT name, salary, ROUND(100 * CUME_DIST() OVER (ORDER BY salary), 1) AS percentile FROM employees",
         "SELECT name, salary, ROUND(100 * PERCENT_RANK() OVER (ORDER BY salary DESC), 1) AS percentile FROM employees"],
  notes="`PERCENT_RANK()` is `(rank − 1) / (rows − 1)`, and 0 when there's only one row.")

P("top-customer-per-city", "Top Customer in Each City", "ranking", "top-per-group", "hard",
  """
  A customer's spend is the sum of `quantity × price` over their **delivered** orders. In each city, find the customer
  who spent the most; list everyone tied for the most. Customers who haven't spent anything don't count.

  Return `city`, `name` and `spent` (rounded to 2 decimal places), ordered by `city`, then `name`.
  """,
  [CUSTOMERS, PRODUCTS, ORDERS, ORDER_ITEMS],
  """
  WITH spend AS (
    SELECT c.city, c.name, SUM(i.quantity * p.price) AS spent
    FROM customers c
    JOIN orders o ON o.customer_id = c.id AND o.status = 'delivered'
    JOIN order_items i ON i.order_id = o.id
    JOIN products p ON p.id = i.product_id
    GROUP BY c.id, c.city, c.name
  ),
  ranked AS (
    SELECT city, name, spent, RANK() OVER (PARTITION BY city ORDER BY spent DESC) AS r FROM spend
  )
  SELECT city, name, ROUND(spent, 2) AS spent FROM ranked WHERE r = 1 ORDER BY city, name
  """,
  [(SHOP_EX, "Omar spent 74.00 in Osaka; Uma, also in Osaka, never ordered. Priya's only order was cancelled and Elif's hasn't been delivered, so Lisbon and Denver have no spenders yet.")],
  lambda rng, n, k: shop(rng, n * 2, k),
  ordered=True,
  wrong=["WITH spend AS (SELECT c.city, c.name, SUM(i.quantity * p.price) AS spent FROM customers c JOIN orders o ON o.customer_id = c.id AND o.status = 'delivered' JOIN order_items i ON i.order_id = o.id JOIN products p ON p.id = i.product_id GROUP BY c.id, c.city, c.name), ranked AS (SELECT city, name, spent, ROW_NUMBER() OVER (PARTITION BY city ORDER BY spent DESC) AS r FROM spend) SELECT city, name, ROUND(spent, 2) AS spent FROM ranked WHERE r = 1 ORDER BY city, name",
         "WITH spend AS (SELECT c.city, c.name, SUM(i.quantity * p.price) AS spent FROM customers c JOIN orders o ON o.customer_id = c.id JOIN order_items i ON i.order_id = o.id JOIN products p ON p.id = i.product_id GROUP BY c.id, c.city, c.name), ranked AS (SELECT city, name, spent, RANK() OVER (PARTITION BY city ORDER BY spent DESC) AS r FROM spend) SELECT city, name, ROUND(spent, 2) AS spent FROM ranked WHERE r = 1 ORDER BY city, name"])

P("pareto-products", "Pareto Products", "window-aggregates", "running-totals", "hard",
  """
  Rank the products by revenue from **delivered** orders (`quantity × price`), highest first, ties by `name`. Only
  products with delivered sales appear. Next to each, show the running share of all that revenue covered so far.

  Return `name`, `revenue` (rounded to 2 decimal places) and `cum_pct` (the running total as a percentage of the grand
  total, rounded to 1 decimal place), in that order.
  """,
  [PRODUCTS, ORDERS, ORDER_ITEMS],
  """
  WITH rev AS (
    SELECT p.name, SUM(i.quantity * p.price) AS revenue
    FROM order_items i
    JOIN orders o ON o.id = i.order_id
    JOIN products p ON p.id = i.product_id
    WHERE o.status = 'delivered'
    GROUP BY p.id, p.name
  )
  SELECT name, ROUND(revenue, 2) AS revenue,
         ROUND(100.0 * SUM(revenue) OVER (ORDER BY revenue DESC, name) / SUM(revenue) OVER (), 1) AS cum_pct
  FROM rev
  ORDER BY revenue DESC, name
  """,
  [(ex(SHOP_EX, "products", "orders", "order_items"), "Delivered revenue is 74.00: the Kettles alone bring 49.00 (66.2%), the Comics take it to 62.00 (83.8%), and the Novel completes it.")],
  lambda rng, n, k: only(shop(rng, n, k), "products", "orders", "order_items"),
  ordered=True,
  wrong=["WITH rev AS (SELECT p.name, SUM(i.quantity * p.price) AS revenue FROM order_items i JOIN orders o ON o.id = i.order_id JOIN products p ON p.id = i.product_id WHERE o.status = 'delivered' GROUP BY p.id, p.name) SELECT name, ROUND(revenue, 2) AS revenue, ROUND(100.0 * SUM(revenue) OVER (ORDER BY revenue DESC) / SUM(revenue) OVER (), 1) AS cum_pct FROM rev ORDER BY revenue DESC, name",
         "WITH rev AS (SELECT p.name, SUM(i.quantity * p.price) AS revenue FROM order_items i JOIN orders o ON o.id = i.order_id JOIN products p ON p.id = i.product_id WHERE o.status = 'delivered' GROUP BY p.id, p.name) SELECT name, ROUND(revenue, 2) AS revenue, ROUND(100.0 * revenue / SUM(revenue) OVER (), 1) AS cum_pct FROM rev ORDER BY revenue DESC, name"])

P("category-revenue-share", "Category Share of Revenue", "window-aggregates", "share-of-total", "medium",
  """
  Revenue is `quantity × price` over orders that **weren't cancelled**. For each category with revenue, return
  `category`, `revenue` (rounded to 2 decimal places) and `share`: its percentage of all revenue, rounded to 1 decimal
  place. Any order.
  """,
  [PRODUCTS, ORDERS, ORDER_ITEMS],
  """
  SELECT p.category,
         ROUND(SUM(i.quantity * p.price), 2) AS revenue,
         ROUND(100.0 * SUM(i.quantity * p.price) / SUM(SUM(i.quantity * p.price)) OVER (), 1) AS share
  FROM order_items i
  JOIN orders o ON o.id = i.order_id
  JOIN products p ON p.id = i.product_id
  WHERE o.status <> 'cancelled'
  GROUP BY p.category
  """,
  [(ex(SHOP_EX, "products", "orders", "order_items"), "Without the cancelled order, revenue is 94.00: Kitchen 49.00 (52.1%), Books 37.00 (39.4%) and Toys 8.00 (8.5%).")],
  lambda rng, n, k: only(shop(rng, n, k), "products", "orders", "order_items"),
  wrong=["SELECT p.category, ROUND(SUM(i.quantity * p.price), 2) AS revenue, ROUND(100.0 * SUM(i.quantity * p.price) / SUM(SUM(i.quantity * p.price)) OVER (), 1) AS share FROM order_items i JOIN products p ON p.id = i.product_id GROUP BY p.category",
         "SELECT p.category, ROUND(SUM(i.quantity * p.price), 2) AS revenue, ROUND(100.0 * SUM(i.quantity * p.price) / SUM(p.price) OVER (), 1) AS share FROM order_items i JOIN orders o ON o.id = i.order_id JOIN products p ON p.id = i.product_id WHERE o.status <> 'cancelled' GROUP BY p.category"],
  notes="Window functions run after `GROUP BY`, so `SUM(SUM(…)) OVER ()` adds up every group's total.")

EVENTS = T("events", ("user_id", "INTEGER"), ("at", "TEXT"))


def events_gen(rng, n, k):
    rows = []
    for u in range(1, max(1, n // 4 + 1) + 1):
        t = rng.randint(0, 1400)
        for _ in range(rng.randint(1, max(1, n // 2))):
            rows.append((u, f"2024-05-{1 + t // 1440:02d} {t % 1440 // 60:02d}:{t % 60:02d}"))
            t += rng.choice([5, 30, 31, 45]) if ties(k) else rng.choice([rng.randint(1, 30), rng.randint(31, 300)])
    rng.shuffle(rows)
    return {"events": rows}

P("views-by-hour", "Views by Hour", "recursive", "series", "medium",
  """
  Count page views by the hour of the day they happened in (`0` for 00:00–00:59 up to `23`). The chart needs **all 24
  hours**, including hours with no views.

  Return `hour` and `views` for hours 0 to 23, ordered by `hour`.
  """,
  [EVENTS],
  """
  WITH RECURSIVE hours(hour) AS (
    SELECT 0
    UNION ALL
    SELECT hour + 1 FROM hours WHERE hour < 23
  )
  SELECT h.hour, COUNT(e.at) AS views
  FROM hours h
  LEFT JOIN events e ON CAST(strftime('%H', e.at) AS INTEGER) = h.hour
  GROUP BY h.hour
  ORDER BY h.hour
  """,
  [({"events": [(1, "2024-05-01 09:00"), (1, "2024-05-01 09:20"), (2, "2024-05-01 13:05"), (2, "2024-05-02 09:45")]},
    "Three views fall in the 9 o'clock hour (on two different days) and one at 13. The other 22 hours show 0.")],
  events_gen,
  ordered=True,
  wrong=["SELECT CAST(strftime('%H', at) AS INTEGER) AS hour, COUNT(*) AS views FROM events GROUP BY hour ORDER BY hour",
         "WITH RECURSIVE hours(hour) AS (SELECT 0 UNION ALL SELECT hour + 1 FROM hours WHERE hour < 23) SELECT h.hour, COUNT(*) AS views FROM hours h LEFT JOIN events e ON CAST(strftime('%H', e.at) AS INTEGER) = h.hour GROUP BY h.hour ORDER BY h.hour"],
  notes="With a LEFT JOIN, an hour with no views still has one row (with NULLs), so count a column from `events`, not `*`.")

P("session-details", "Session Details", "gaps-islands", "sessions", "hard",
  """
  A user's page views form one **session** until there's a gap of **more than 30 minutes** (exactly 30 stays in the same
  session). Number each user's sessions from 1 in time order.

  Return `user_id`, `session`, `started_at` (first view), `ended_at` (last view) and `views`, ordered by `user_id`, then
  `session`.
  """,
  [EVENTS],
  """
  WITH flagged AS (
    SELECT user_id, at,
           CASE WHEN (strftime('%s', at) - strftime('%s', LAG(at) OVER (PARTITION BY user_id ORDER BY at))) / 60 <= 30
                THEN 0 ELSE 1 END AS starts
    FROM events
  ),
  numbered AS (
    SELECT user_id, at, SUM(starts) OVER (PARTITION BY user_id ORDER BY at ROWS UNBOUNDED PRECEDING) AS session
    FROM flagged
  )
  SELECT user_id, session, MIN(at) AS started_at, MAX(at) AS ended_at, COUNT(*) AS views
  FROM numbered
  GROUP BY user_id, session
  ORDER BY user_id, session
  """,
  [({"events": [(1, "2024-05-01 09:00"), (1, "2024-05-01 09:20"), (1, "2024-05-01 09:50"), (1, "2024-05-01 10:30"), (2, "2024-05-01 12:00")]},
    "User 1's first session runs 9:00–9:50 (the last gap is exactly 30 minutes) with 3 views; 10:30 starts session 2.")],
  events_gen,
  ordered=True,
  wrong=["WITH flagged AS (SELECT user_id, at, CASE WHEN (strftime('%s', at) - strftime('%s', LAG(at) OVER (PARTITION BY user_id ORDER BY at))) / 60 < 30 THEN 0 ELSE 1 END AS starts FROM events), numbered AS (SELECT user_id, at, SUM(starts) OVER (PARTITION BY user_id ORDER BY at ROWS UNBOUNDED PRECEDING) AS session FROM flagged) SELECT user_id, session, MIN(at) AS started_at, MAX(at) AS ended_at, COUNT(*) AS views FROM numbered GROUP BY user_id, session ORDER BY user_id, session",
         "WITH flagged AS (SELECT user_id, at, CASE WHEN (strftime('%s', at) - strftime('%s', LAG(at) OVER (PARTITION BY user_id ORDER BY at))) / 60 <= 30 THEN 0 ELSE 1 END AS starts FROM events), numbered AS (SELECT user_id, at, SUM(starts) OVER (ORDER BY at ROWS UNBOUNDED PRECEDING) AS session FROM flagged) SELECT user_id, session, MIN(at) AS started_at, MAX(at) AS ended_at, COUNT(*) AS views FROM numbered GROUP BY user_id, session ORDER BY user_id, session"],
  notes="Flag the row that starts each session with 1, then a running sum of the flags numbers the sessions.")

LOGINS = T("logins", ("user_id", "INTEGER"), ("login_on", "TEXT"))

P("days-without-logins", "Days Without Logins", "gaps-islands", "missing-ranges", "hard",
  """
  Between each user's first and last login, find the **runs of days with no login**. A user may log in several times a
  day.

  Return `user_id`, `gap_start` and `gap_end` (the first and last day of each run), ordered by `user_id`, then
  `gap_start`.
  """,
  [LOGINS],
  """
  WITH days AS (
    SELECT DISTINCT user_id, login_on FROM logins
  ),
  nexts AS (
    SELECT user_id, login_on, LEAD(login_on) OVER (PARTITION BY user_id ORDER BY login_on) AS next_on FROM days
  )
  SELECT user_id, date(login_on, '+1 day') AS gap_start, date(next_on, '-1 day') AS gap_end
  FROM nexts
  WHERE julianday(next_on) - julianday(login_on) > 1
  ORDER BY user_id, gap_start
  """,
  [({"logins": [(1, "2024-01-01"), (1, "2024-01-02"), (1, "2024-01-05"), (1, "2024-01-05"), (1, "2024-01-06"), (1, "2024-01-09"), (2, "2024-01-03"), (2, "2024-01-04")]},
    "User 1 skipped January 3–4 and January 7–8. User 2 logged in on two days in a row, so there's no gap.")],
  lambda rng, n, k: only(app(rng, n * 2, k), "logins"),
  ordered=True,
  wrong=["WITH days AS (SELECT DISTINCT user_id, login_on FROM logins), nexts AS (SELECT user_id, login_on, LEAD(login_on) OVER (ORDER BY login_on) AS next_on FROM days) SELECT user_id, date(login_on, '+1 day') AS gap_start, date(next_on, '-1 day') AS gap_end FROM nexts WHERE julianday(next_on) - julianday(login_on) > 1 ORDER BY user_id, gap_start",
         "WITH days AS (SELECT DISTINCT user_id, login_on FROM logins), nexts AS (SELECT user_id, login_on, LEAD(login_on) OVER (PARTITION BY user_id ORDER BY login_on) AS next_on FROM days) SELECT user_id, login_on AS gap_start, next_on AS gap_end FROM nexts WHERE julianday(next_on) - julianday(login_on) > 1 ORDER BY user_id, gap_start"])


def year_grid_gen(rng, n, k):
    d = school(rng, n, k)
    ids = [c[0] for c in d["courses"]]
    if k % 3 and len(ids) > 1:  # a course nobody takes still gets a row
        empty = rng.choice(ids)
        d["enrollments"] = [e for e in d["enrollments"] if e[1] != empty]
    return d

P("enrollment-by-year", "Enrollment by Year", "reporting", "pivot", "medium",
  """
  Students are in `year` 1 to 4. For **every** course, count its enrolled students by year, one column per year.

  Return `title`, `y1`, `y2`, `y3` and `y4` (`0` where there are none), ordered by `title`.
  """,
  [STUDENTS, COURSES, ENROLLMENTS],
  """
  SELECT c.title,
         SUM(CASE WHEN s.year = 1 THEN 1 ELSE 0 END) AS y1,
         SUM(CASE WHEN s.year = 2 THEN 1 ELSE 0 END) AS y2,
         SUM(CASE WHEN s.year = 3 THEN 1 ELSE 0 END) AS y3,
         SUM(CASE WHEN s.year = 4 THEN 1 ELSE 0 END) AS y4
  FROM courses c
  LEFT JOIN enrollments e ON e.course_id = c.id
  LEFT JOIN students s ON s.id = e.student_id
  GROUP BY c.id, c.title
  ORDER BY c.title
  """,
  [(SCHOOL_EX, "Algebra has Ava (year 1) and Bilal (year 2). Biology has Ava. Nobody takes Drawing, so it's all zeros.")],
  year_grid_gen,
  ordered=True,
  wrong=["SELECT c.title, SUM(CASE WHEN s.year = 1 THEN 1 ELSE 0 END) AS y1, SUM(CASE WHEN s.year = 2 THEN 1 ELSE 0 END) AS y2, SUM(CASE WHEN s.year = 3 THEN 1 ELSE 0 END) AS y3, SUM(CASE WHEN s.year = 4 THEN 1 ELSE 0 END) AS y4 FROM courses c JOIN enrollments e ON e.course_id = c.id JOIN students s ON s.id = e.student_id GROUP BY c.id, c.title ORDER BY c.title",
         "SELECT c.title, COUNT(CASE WHEN s.year = 1 THEN 1 ELSE 0 END) AS y1, COUNT(CASE WHEN s.year = 2 THEN 1 ELSE 0 END) AS y2, COUNT(CASE WHEN s.year = 3 THEN 1 ELSE 0 END) AS y3, COUNT(CASE WHEN s.year = 4 THEN 1 ELSE 0 END) AS y4 FROM courses c LEFT JOIN enrollments e ON e.course_id = c.id LEFT JOIN students s ON s.id = e.student_id GROUP BY c.id, c.title ORDER BY c.title"])

done()
