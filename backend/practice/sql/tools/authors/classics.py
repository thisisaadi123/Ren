"""A second problem for many patterns: the questions interviews ask most often, in Ren's own settings."""
import _common  # noqa: F401
from _common import only
from author import FIRST, P, T, day, done, firsts, names
from worlds import ENROLLMENTS, EMPLOYEES, ORDER_ITEMS, ORDERS, PRODUCTS, CUSTOMERS, USERS, app, school, shop, staff, ties

EMP_EX = {"employees": [
    (1, "Ava Moss", 1, None, 96000, "2019-03-04"),
    (2, "Bilal Cruz", 2, 1, 61000, "2020-07-15"),
    (3, "Chen Ito", 1, 1, 60000, "2021-01-10"),
    (4, "Dara Kerr", None, 2, 125500, "2019-03-04"),
    (5, "Elif Park", 2, 2, 48000, "2022-11-30"),
]}
SHOP_EX = {
    "customers": [(1, "Omar Fox", "Osaka", "2023-02-01"), (2, "Priya Nair", "Lisbon", "2023-05-12"),
                  (3, "Elif Gray", "Denver", "2023-01-20"), (4, "Uma Sato", "Osaka", "2023-08-03")],
    "products": [(1, "Kettle", "Kitchen", 24.5), (2, "Novel", "Books", 12.0), (3, "Kite", "Toys", 8.0), (4, "Comic", "Books", 6.5)],
    "orders": [(1, 1, "2024-01-03", "delivered"), (2, 2, "2024-01-04", "cancelled"),
               (3, 1, "2024-02-10", "delivered"), (4, 3, "2024-02-11", "shipped")],
    "order_items": [(1, 1, 2), (1, 2, 1), (2, 3, 3), (3, 4, 2), (4, 2, 1), (4, 3, 1)],
}
ex = lambda data, *tables: only(data, *tables)  # noqa: E731

P("price-with-tax", "Price with Tax", "select-filter", "pick-columns", "easy",
  """
  Shelf labels show prices with **20% sales tax** added.

  Return each product's `name`, its `price`, and `with_tax`: the price times 1.2, rounded to 2 decimal places. Any
  order.
  """,
  [PRODUCTS],
  "SELECT name, price, ROUND(price * 1.2, 2) AS with_tax FROM products",
  [(ex(SHOP_EX, "products"), "The Kettle's 24.50 becomes 29.40; the Comic's 6.50 becomes 7.80.")],
  lambda rng, n, k: only(shop(rng, n * 2, k), "products"),
  wrong=["SELECT name, price, ROUND(price + 0.2, 2) AS with_tax FROM products",
         "SELECT name, price, ROUND(price * 0.2, 2) AS with_tax FROM products"])


def march_gen(rng, n, k):
    d = only(shop(rng, n * 2, k, start=(2024, 2, 20), span=50), "orders")
    if k % 2 == 0:
        d["orders"].append((len(d["orders"]) + 1, 1, "2024-03-31", "delivered"))
        d["orders"].append((len(d["orders"]) + 1, 1, "2024-03-01", "shipped"))
    return d

P("march-orders", "Orders Placed in March", "select-filter", "where-conditions", "easy",
  """
  Return the `id` and `ordered_on` of every order placed in **March 2024** (from the 1st to the 31st, both included)
  that **wasn't cancelled**. Any order.
  """,
  [ORDERS],
  "SELECT id, ordered_on FROM orders WHERE ordered_on BETWEEN '2024-03-01' AND '2024-03-31' AND status <> 'cancelled'",
  [({"orders": [(1, 1, "2024-02-29", "delivered"), (2, 2, "2024-03-01", "shipped"), (3, 1, "2024-03-18", "cancelled"),
                (4, 3, "2024-03-31", "delivered"), (5, 2, "2024-04-01", "delivered")]},
    "Orders 2 and 4 are in March and still active. Order 3 is in March but was cancelled.")],
  march_gen,
  wrong=["SELECT id, ordered_on FROM orders WHERE ordered_on > '2024-03-01' AND ordered_on < '2024-03-31' AND status <> 'cancelled'",
         "SELECT id, ordered_on FROM orders WHERE ordered_on BETWEEN '2024-03-01' AND '2024-03-31'"])

P("missing-scores", "Missing Scores", "select-filter", "null-checks", "medium",
  """
  Teachers enter a `score` for each enrollment once the exam is marked; until then it's NULL.

  For every course that has enrollments, return `course_id`, `enrolled` (how many students), `scored` (how many have a
  score) and `missing` (how many don't). Any order.
  """,
  [ENROLLMENTS],
  "SELECT course_id, COUNT(*) AS enrolled, COUNT(score) AS scored, COUNT(*) - COUNT(score) AS missing FROM enrollments GROUP BY course_id",
  [({"enrollments": [(1, 1, 88), (1, 2, None), (2, 1, 72), (3, 1, None), (3, 2, 64)]},
    "Course 1 has three students, one still unmarked. Course 2 has two, one unmarked.")],
  lambda rng, n, k: only(school(rng, n, 1), "enrollments"),
  wrong=["SELECT course_id, COUNT(score) AS enrolled, COUNT(score) AS scored, 0 AS missing FROM enrollments GROUP BY course_id",
         "SELECT course_id, COUNT(*) AS enrolled, COUNT(*) AS scored, SUM(score = NULL) AS missing FROM enrollments GROUP BY course_id"],
  notes="`COUNT(*)` counts rows; `COUNT(score)` counts only the rows where `score` isn't NULL.")

P("status-first", "Shipping First", "sort-limit", "order-by", "easy",
  """
  The warehouse screen lists orders by status in this order: `'shipped'` first, then `'delivered'`, then `'cancelled'`.
  Within a status, the newest orders come first, and orders from the same day go by `id`.

  Return `id`, `status` and `ordered_on` in that order.
  """,
  [ORDERS],
  """
  SELECT id, status, ordered_on
  FROM orders
  ORDER BY CASE status WHEN 'shipped' THEN 1 WHEN 'delivered' THEN 2 ELSE 3 END,
           ordered_on DESC,
           id
  """,
  [(ex(SHOP_EX, "orders"), "Order 4 is the only one shipping. Then the delivered orders, newest first (3, then 1). The cancelled order goes last.")],
  lambda rng, n, k: only(shop(rng, n * 2, k, span=max(2, n // 2)), "orders"),
  ordered=True,
  wrong=["SELECT id, status, ordered_on FROM orders ORDER BY status, ordered_on DESC, id",
         "SELECT id, status, ordered_on FROM orders ORDER BY CASE status WHEN 'shipped' THEN 1 WHEN 'delivered' THEN 2 ELSE 3 END, ordered_on, id"])


def second_gen(rng, n, k):
    d = only(staff(rng, n, k), "employees")
    if k % 4 == 1:  # everyone earns the same: there's no second-highest salary
        d["employees"] = [r[:4] + (70000,) + r[5:] for r in d["employees"]]
    return d

P("second-highest-salary", "Second-highest Salary", "sort-limit", "top-n", "medium",
  """
  Find the **second-highest distinct salary** at the company. If several people share the top salary, the next lower
  salary is second.

  Return one row with one column, `second_highest`. If there's no second-highest salary (one distinct salary or
  none), return NULL in that row.
  """,
  [EMPLOYEES],
  "SELECT (SELECT DISTINCT salary FROM employees ORDER BY salary DESC LIMIT 1 OFFSET 1) AS second_highest",
  [(EMP_EX, "Salaries from the top: 125,500, 96,000, … The second-highest is 96,000."),
   ({"employees": [(1, "Ava Moss", 1, None, 80000, "2020-01-01"), (2, "Bilal Cruz", 1, 1, 80000, "2021-01-01")]},
    "Both earn 80,000, so there's only one distinct salary: the answer is NULL.")],
  second_gen,
  wrong=["SELECT salary AS second_highest FROM employees ORDER BY salary DESC LIMIT 1 OFFSET 1",
         "SELECT DISTINCT salary AS second_highest FROM employees ORDER BY salary DESC LIMIT 1 OFFSET 1"],
  notes="A query that finds no row returns no row at all. Wrapping it as a subquery in `SELECT (…)` turns \"no row\" into a single NULL.")

P("buyers-per-day", "Buyers per Day", "sort-limit", "distinct-values", "easy",
  """
  Some customers order more than once a day. For each day with orders, count the **different customers** who ordered.

  Return `ordered_on` and `buyers`, ordered by `ordered_on`.
  """,
  [ORDERS],
  "SELECT ordered_on, COUNT(DISTINCT customer_id) AS buyers FROM orders GROUP BY ordered_on ORDER BY ordered_on",
  [({"orders": [(1, 1, "2024-01-03", "delivered"), (2, 1, "2024-01-03", "shipped"), (3, 2, "2024-01-03", "delivered"), (4, 2, "2024-01-04", "delivered")]},
    "Three orders on January 3, but only two different customers.")],
  lambda rng, n, k: only(shop(rng, n * 2, k, span=max(2, n // 3)), "orders"),
  ordered=True,
  wrong=["SELECT ordered_on, COUNT(*) AS buyers FROM orders GROUP BY ordered_on ORDER BY ordered_on",
         "SELECT ordered_on, COUNT(DISTINCT id) AS buyers FROM orders GROUP BY ordered_on ORDER BY ordered_on"])

P("cancellation-rate", "Cancellation Rate", "conditional", "conditional-aggregation", "medium",
  """
  For each month (written `YYYY-MM`), return `month`, `orders` (all orders placed), `cancelled` (how many were
  cancelled) and `rate`: the percentage cancelled, rounded to 1 decimal place. Order by `month`.
  """,
  [ORDERS],
  """
  SELECT strftime('%Y-%m', ordered_on) AS month,
         COUNT(*) AS orders,
         SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled,
         ROUND(100.0 * SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) / COUNT(*), 1) AS rate
  FROM orders
  GROUP BY month
  ORDER BY month
  """,
  [({"orders": [(1, 1, "2024-01-03", "cancelled"), (2, 2, "2024-01-09", "delivered"), (3, 1, "2024-01-20", "delivered"),
                (4, 3, "2024-02-02", "delivered")]},
    "January had 3 orders and 1 cancellation: 33.3%. February had no cancellations.")],
  lambda rng, n, k: only(shop(rng, n * 2, k, span=150), "orders"),
  ordered=True,
  wrong=["SELECT strftime('%Y-%m', ordered_on) AS month, COUNT(*) AS orders, SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled, ROUND(100 * SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) / COUNT(*), 1) AS rate FROM orders GROUP BY month ORDER BY month",
         "SELECT strftime('%Y-%m', ordered_on) AS month, COUNT(*) AS orders, SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled, ROUND(SUM(CASE WHEN status = 'cancelled' THEN 1.0 ELSE 0 END) / COUNT(*), 1) AS rate FROM orders GROUP BY month ORDER BY month"])


def every_category_gen(rng, n, k):
    d = shop(rng, n * 2, k)
    cats = sorted({p[2] for p in d["products"]})
    if k % 3 != 1:
        # One or two customers sweep the whole catalogue in a single order.
        for cust in rng.sample([c[0] for c in d["customers"]], min(2, len(d["customers"]))):
            oid = len(d["orders"]) + 1
            d["orders"].append((oid, cust, "2024-07-01", "delivered"))
            for cat in cats:
                pid = rng.choice([p[0] for p in d["products"] if p[2] == cat])
                d["order_items"].append((oid, pid, 1))
    if k % 3 == 2 and len(d["products"]) > len(cats):
        # A category nobody has bought from yet still counts.
        d["products"].append((len(d["products"]) + 1, "Globe", "Maps", 15.0))
    return d

P("bought-every-category", "Bought from Every Category", "aggregation", "having", "hard",
  """
  Find the customers who have bought at least one product from **every category in the catalogue**, counting only
  orders that weren't cancelled.

  Return each such customer's `name`, in any order.
  """,
  [CUSTOMERS, PRODUCTS, ORDERS, ORDER_ITEMS],
  """
  SELECT c.name
  FROM customers c
  JOIN orders o ON o.customer_id = c.id AND o.status <> 'cancelled'
  JOIN order_items i ON i.order_id = o.id
  JOIN products p ON p.id = i.product_id
  GROUP BY c.id, c.name
  HAVING COUNT(DISTINCT p.category) = (SELECT COUNT(DISTINCT category) FROM products)
  """,
  [({"customers": SHOP_EX["customers"], "products": SHOP_EX["products"],
     "orders": SHOP_EX["orders"] + [(5, 3, "2024-02-12", "delivered")],
     "order_items": SHOP_EX["order_items"] + [(5, 1, 1)]},
    "There are three categories. Elif's orders cover Books, Toys and (with order 5) Kitchen. Omar never bought a Toy, and Priya's only order was cancelled.")],
  every_category_gen,
  wrong=["SELECT c.name FROM customers c JOIN orders o ON o.customer_id = c.id AND o.status <> 'cancelled' JOIN order_items i ON i.order_id = o.id JOIN products p ON p.id = i.product_id GROUP BY c.id, c.name HAVING COUNT(p.category) = (SELECT COUNT(DISTINCT category) FROM products)",
         "SELECT c.name FROM customers c JOIN orders o ON o.customer_id = c.id AND o.status <> 'cancelled' JOIN order_items i ON i.order_id = o.id JOIN products p ON p.id = i.product_id GROUP BY c.id, c.name HAVING COUNT(DISTINCT p.category) = (SELECT COUNT(DISTINCT p2.category) FROM order_items i2 JOIN products p2 ON p2.id = i2.product_id)"],
  sizes=[2, 3, 4, 6, 8, 10, 14, 20, 30, 45, 70, 100, 150, 220])

P("products-never-sold", "Products Never Sold", "joins", "anti-join", "easy",
  """
  Return the `name` of every product that doesn't appear in **any** order, in alphabetical order.
  """,
  [PRODUCTS, ORDER_ITEMS],
  "SELECT p.name FROM products p LEFT JOIN order_items i ON i.product_id = p.id WHERE i.product_id IS NULL ORDER BY p.name",
  [({"products": SHOP_EX["products"] + [(5, "Globe", "Maps", 15.0)], "order_items": SHOP_EX["order_items"]},
    "Every product has been ordered except the Globe.")],
  lambda rng, n, k: (lambda d: {"products": d["products"] + [(len(d["products"]) + 1, "Globe", "Maps", 15.0)] if k % 4 else d["products"], "order_items": d["order_items"]})(only(shop(rng, max(1, n // 2), k), "products", "order_items")),
  ordered=True,
  wrong=["SELECT p.name FROM products p JOIN order_items i ON i.product_id = p.id WHERE i.quantity = 0 ORDER BY p.name",
         "SELECT p.name FROM products p WHERE p.id NOT IN (SELECT order_id FROM order_items) ORDER BY p.name"])

P("bought-together", "Bought Together", "joins", "self-join", "hard",
  """
  Find pairs of products that are often bought **in the same order**.

  For every pair of different products that appear together in **at least 2** orders, return `product_a` and
  `product_b` (their names, with the smaller product `id` as `product_a`) and `orders` (how many orders contain both).
  Order by `orders` from most to least, then `product_a`, then `product_b`.
  """,
  [PRODUCTS, ORDER_ITEMS],
  """
  SELECT pa.name AS product_a, pb.name AS product_b, COUNT(*) AS orders
  FROM order_items a
  JOIN order_items b ON b.order_id = a.order_id AND a.product_id < b.product_id
  JOIN products pa ON pa.id = a.product_id
  JOIN products pb ON pb.id = b.product_id
  GROUP BY a.product_id, b.product_id, pa.name, pb.name
  HAVING COUNT(*) >= 2
  ORDER BY orders DESC, product_a, product_b
  """,
  [({"products": SHOP_EX["products"], "order_items": [(1, 1, 2), (1, 2, 1), (2, 1, 1), (2, 2, 3), (2, 3, 1), (3, 2, 1), (3, 3, 2)]},
    "The Kettle and the Novel share orders 1 and 2. The Novel and the Kite share orders 2 and 3. The Kettle and the Kite only share order 2.")],
  lambda rng, n, k: only(shop(rng, n * 2, k), "products", "order_items"),
  ordered=True,
  wrong=["SELECT pa.name AS product_a, pb.name AS product_b, COUNT(*) AS orders FROM order_items a JOIN order_items b ON b.order_id = a.order_id AND a.product_id <> b.product_id JOIN products pa ON pa.id = a.product_id JOIN products pb ON pb.id = b.product_id GROUP BY a.product_id, b.product_id, pa.name, pb.name HAVING COUNT(*) >= 2 ORDER BY orders DESC, product_a, product_b",
         "SELECT pa.name AS product_a, pb.name AS product_b, COUNT(*) AS orders FROM order_items a JOIN order_items b ON b.order_id = a.order_id AND a.product_id < b.product_id JOIN products pa ON pa.id = a.product_id JOIN products pb ON pb.id = b.product_id GROUP BY a.product_id, b.product_id, pa.name, pb.name ORDER BY orders DESC, product_a, product_b"])

FRIENDSHIPS = T("friendships", ("a", "INTEGER"), ("b", "INTEGER"))


def friends_gen(rng, n, k):
    people = max(2, n // 2 + 2)
    pairs = set()
    while len(pairs) < min(n, people * (people - 1) // 2):
        x, y = rng.sample(range(1, people + 1), 2)
        pairs.add((min(x, y), max(x, y)))
    rows = [(x, y) if rng.random() < 0.5 else (y, x) for x, y in pairs]
    return {"friendships": rows}

P("most-friends", "Most Friends", "set-ops", "union", "medium",
  """
  Each row of `friendships` is one friendship between users `a` and `b`, stored once, in either direction.

  Return the `user_id` and `friends` (number of friends) of the user with the **most friends**. If several users tie,
  return them all, ordered by `user_id`.
  """,
  [FRIENDSHIPS],
  """
  WITH ends AS (
    SELECT a AS user_id FROM friendships
    UNION ALL
    SELECT b FROM friendships
  ),
  counts AS (
    SELECT user_id, COUNT(*) AS friends FROM ends GROUP BY user_id
  )
  SELECT user_id, friends FROM counts
  WHERE friends = (SELECT MAX(friends) FROM counts)
  ORDER BY user_id
  """,
  [({"friendships": [(1, 2), (3, 1), (2, 3), (4, 3)]},
    "User 3 is in three friendships (with 1, 2 and 4). Users 1 and 2 have two friends each, user 4 has one.")],
  friends_gen,
  ordered=True,
  wrong=["WITH counts AS (SELECT a AS user_id, COUNT(*) AS friends FROM friendships GROUP BY a) SELECT user_id, friends FROM counts WHERE friends = (SELECT MAX(friends) FROM counts) ORDER BY user_id",
         "WITH ends AS (SELECT a AS user_id FROM friendships UNION SELECT b FROM friendships), counts AS (SELECT user_id, COUNT(*) AS friends FROM ends GROUP BY user_id) SELECT user_id, friends FROM counts WHERE friends = (SELECT MAX(friends) FROM counts) ORDER BY user_id"])

P("above-category-average", "Pricier Than Their Category", "subqueries", "correlated", "medium",
  """
  Return the `category`, `name` and `price` of every product that costs **more than the average price of its own
  category**, in any order.
  """,
  [PRODUCTS],
  "SELECT category, name, price FROM products p WHERE price > (SELECT AVG(price) FROM products q WHERE q.category = p.category)",
  [(ex(SHOP_EX, "products"), "Books average (12.00 + 6.50) / 2 = 9.25, so the Novel qualifies. The Kettle and the Kite are alone in their categories, so they equal their own average.")],
  lambda rng, n, k: only(shop(rng, n * 2, k), "products"),
  wrong=["SELECT category, name, price FROM products WHERE price > (SELECT AVG(price) FROM products)",
         "SELECT category, name, price FROM products p WHERE price >= (SELECT AVG(price) FROM products q WHERE q.category = p.category)"])

DAILY = T("daily_sales", ("day", "TEXT", "pk"), ("revenue", "INTEGER"))

P("rolling-week", "Rolling Week", "window-aggregates", "moving-windows", "medium",
  """
  `daily_sales` has one row for every day, with no gaps. For each day that has **six full days before it**, return the
  total revenue of that day and the six before it.

  Return `day` and `week_total`, ordered by `day`. The first six days don't appear.
  """,
  [DAILY],
  """
  SELECT day, week_total
  FROM (
    SELECT day,
           SUM(revenue) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS week_total,
           ROW_NUMBER() OVER (ORDER BY day) AS rn
    FROM daily_sales
  )
  WHERE rn >= 7
  ORDER BY day
  """,
  [({"daily_sales": [(day(i, (2024, 4, 1)), v) for i, v in enumerate([5, 10, 0, 20, 5, 10, 30, 40])]},
    "April 7 is the first day with a full week: 5 + 10 + 0 + 20 + 5 + 10 + 30 = 80. April 8 drops April 1 and adds 40: 115.")],
  lambda rng, n, k: {"daily_sales": [(day(i, (2024, 1, 1)), rng.choice([0, 10]) if ties(k) else rng.randint(0, 300)) for i in range(n + 6)]},
  ordered=True,
  wrong=["SELECT day, SUM(revenue) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS week_total FROM daily_sales ORDER BY day",
         "SELECT day, week_total FROM (SELECT day, SUM(revenue) OVER (ORDER BY day ROWS BETWEEN 7 PRECEDING AND CURRENT ROW) AS week_total, ROW_NUMBER() OVER (ORDER BY day) AS rn FROM daily_sales) WHERE rn >= 7 ORDER BY day"])

MONTHLY = T("monthly_revenue", ("month", "TEXT", "pk"), ("revenue", "INTEGER"))


def monthly_gen(rng, n, k):
    rows, y, m = [], 2022, rng.randint(1, 12)
    for _ in range(n + 1):
        rows.append((f"{y}-{m:02d}", rng.choice([100, 200]) if ties(k) else rng.randint(50, 900)))
        m += 1
        if m > 12:
            y, m = y + 1, 1
    return {"monthly_revenue": rows}

P("month-over-month", "Month-over-month Growth", "window-aggregates", "lag-lead", "medium",
  """
  `monthly_revenue` has one row per month (`YYYY-MM`), with no gaps. Show how revenue grew compared with the month
  before.

  Return `month`, `revenue` and `growth`: the change from the previous month as a percentage of the previous month,
  rounded to 1 decimal place (NULL for the first month). Order by `month`.
  """,
  [MONTHLY],
  """
  SELECT month, revenue,
         ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month)) / LAG(revenue) OVER (ORDER BY month), 1) AS growth
  FROM monthly_revenue
  ORDER BY month
  """,
  [({"monthly_revenue": [("2024-01", 200), ("2024-02", 250), ("2024-03", 150)]},
    "February grew by 50 on 200: 25.0%. March fell by 100 on 250: −40.0%.")],
  monthly_gen,
  ordered=True,
  wrong=["SELECT month, revenue, ROUND(100 * (revenue - LAG(revenue) OVER (ORDER BY month)) / LAG(revenue) OVER (ORDER BY month), 1) AS growth FROM monthly_revenue ORDER BY month",
         "SELECT month, revenue, ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month)) / revenue, 1) AS growth FROM monthly_revenue ORDER BY month"])

SCORES = T("scores", ("player", "TEXT"), ("points", "INTEGER"))

P("top-quarter", "Top Quarter", "reporting", "median-percentile", "medium",
  """
  Sort players by `points` (highest first; equal points by `player`, A to Z) and split them into **4 groups** as evenly
  as possible, with the earlier groups taking any extra players. The first group is the top quarter.

  Return `player` and `points` for the top quarter, in the same sorted order.
  """,
  [SCORES],
  """
  SELECT player, points
  FROM (SELECT player, points, NTILE(4) OVER (ORDER BY points DESC, player) AS quarter FROM scores)
  WHERE quarter = 1
  ORDER BY points DESC, player
  """,
  [({"scores": [("Kai", 90), ("Lena", 85), ("Mina", 90), ("Noor", 70), ("Otto", 85), ("Pia", 60)]},
    "Six players make groups of 2, 2, 1 and 1. The first group is Kai and Mina (90 each, by name).")],
  lambda rng, n, k: {"scores": [(p, rng.choice([70, 80, 90]) if ties(k) else rng.randint(0, 100)) for p in firsts(rng, n)]},
  ordered=True,
  wrong=["SELECT player, points FROM (SELECT player, points, NTILE(4) OVER (ORDER BY points, player) AS quarter FROM scores) WHERE quarter = 1 ORDER BY points DESC, player",
         "SELECT player, points FROM scores ORDER BY points DESC, player LIMIT (SELECT COUNT(*) / 4 FROM scores)"],
  notes="`NTILE(4)` hands out group numbers 1 to 4 in the window's order, as evenly as it can.")

ROLLS = T("rolls", ("id", "INTEGER", "pk"), ("value", "INTEGER"))


def rolls_gen(rng, n, k):
    values = [rng.randint(1, 2 if ties(k) else 6) for _ in range(n + 4)]
    if k % 4 != 3:  # plant one run of three (or more)
        at = rng.randint(0, len(values) - 3)
        values[at:at + 3] = [rng.randint(1, 6)] * 3
    return {"rolls": [(i + 1, v) for i, v in enumerate(values)]}

P("three-in-a-row", "Three in a Row", "gaps-islands", "streaks", "medium",
  """
  A die was rolled many times; `id` is the roll's number (1, 2, 3… with no gaps). Find every value that came up **at
  least three times in a row** somewhere in the log.

  Return each such `value` once, ordered by `value`.
  """,
  [ROLLS],
  """
  SELECT DISTINCT value
  FROM (SELECT value, LAG(value) OVER (ORDER BY id) AS prev, LEAD(value) OVER (ORDER BY id) AS next FROM rolls)
  WHERE value = prev AND value = next
  ORDER BY value
  """,
  [({"rolls": [(i + 1, v) for i, v in enumerate([4, 4, 4, 4, 2, 6, 6, 3, 3, 3])]},
    "4 came up four times in a row and 3 three times. 6 only came up twice in a row.")],
  lambda rng, n, k: rolls_gen(rng, n, k),
  ordered=True,
  wrong=["SELECT value FROM (SELECT value, LAG(value) OVER (ORDER BY id) AS prev, LEAD(value) OVER (ORDER BY id) AS next FROM rolls) WHERE value = prev AND value = next ORDER BY value",
         "SELECT DISTINCT value FROM (SELECT value, LAG(value) OVER (ORDER BY id) AS prev FROM rolls) WHERE value = prev ORDER BY value"])

LOGINS = T("logins", ("user_id", "INTEGER"), ("login_on", "TEXT"))

P("logins-per-active-user", "Logins per Active User", "ctes", "step-ctes", "medium",
  """
  For each month (written `YYYY-MM`), a user is **active** if they logged in at least once. Return `month`, `active`
  (the number of active users) and `avg_logins`: on average, how many times an active user logged in that month,
  rounded to 2 decimal places. Every login row counts. Order by `month`.
  """,
  [LOGINS],
  """
  WITH per_user AS (
    SELECT strftime('%Y-%m', login_on) AS month, user_id, COUNT(*) AS logins
    FROM logins
    GROUP BY month, user_id
  )
  SELECT month, COUNT(*) AS active, ROUND(AVG(logins), 2) AS avg_logins
  FROM per_user
  GROUP BY month
  ORDER BY month
  """,
  [({"logins": [(1, "2024-01-03"), (1, "2024-01-03"), (1, "2024-01-20"), (2, "2024-01-21"), (2, "2024-02-02")]},
    "In January, user 1 logged in 3 times and user 2 once: 2 active users, 2.00 logins each on average.")],
  lambda rng, n, k: only(app(rng, n * 2, k, days=120), "logins"),
  ordered=True,
  wrong=["SELECT strftime('%Y-%m', login_on) AS month, COUNT(*) AS active, ROUND(COUNT(*) * 1.0 / COUNT(*), 2) AS avg_logins FROM logins GROUP BY month ORDER BY month",
         "WITH per_user AS (SELECT strftime('%Y-%m', login_on) AS month, user_id, COUNT(DISTINCT login_on) AS logins FROM logins GROUP BY month, user_id) SELECT month, COUNT(*) AS active, ROUND(AVG(logins), 2) AS avg_logins FROM per_user GROUP BY month ORDER BY month"])

P("orders-by-weekday", "Orders by Weekday", "strings-dates", "date-functions", "easy",
  """
  Count orders by the day of the week they were placed. Number the weekdays the way SQLite does: Sunday is `0`,
  Monday `1`, through Saturday `6`.

  Return `weekday` and `orders` for every weekday that has orders, ordered by `weekday`.
  """,
  [ORDERS],
  "SELECT CAST(strftime('%w', ordered_on) AS INTEGER) AS weekday, COUNT(*) AS orders FROM orders GROUP BY weekday ORDER BY weekday",
  [(ex(SHOP_EX, "orders"), "January 3 and February 10 2024 were a Wednesday and a Saturday; January 4 a Thursday; February 11 a Sunday.")],
  lambda rng, n, k: only(shop(rng, n * 2, k, span=90), "orders"),
  ordered=True,
  wrong=["SELECT CAST(strftime('%d', ordered_on) AS INTEGER) % 7 AS weekday, COUNT(*) AS orders FROM orders GROUP BY weekday ORDER BY weekday",
         "SELECT CAST(strftime('%w', ordered_on) AS INTEGER) AS weekday, COUNT(DISTINCT customer_id) AS orders FROM orders GROUP BY weekday ORDER BY weekday"],
  notes="`strftime('%w', d)` gives the weekday as text, `'0'` (Sunday) to `'6'`; `CAST(… AS INTEGER)` makes it a number.")

LOGINS_U = T("logins", ("user_id", "INTEGER", "fk users.id"), ("login_on", "TEXT"))

P("monthly-cohorts", "Monthly Cohorts", "reporting", "retention", "hard",
  """
  Group users into **cohorts** by the month they signed up (written `YYYY-MM`). A user is **retained** if they logged in
  at least once during the **next calendar month** after their signup month.

  Return `cohort`, `users` (how many signed up that month) and `retained`, ordered by `cohort`.
  """,
  [USERS, LOGINS_U],
  """
  SELECT strftime('%Y-%m', u.signed_up) AS cohort,
         COUNT(*) AS users,
         SUM(EXISTS (
           SELECT 1 FROM logins l
           WHERE l.user_id = u.id
             AND strftime('%Y-%m', l.login_on) = strftime('%Y-%m', u.signed_up, 'start of month', '+1 month')
         )) AS retained
  FROM users u
  GROUP BY cohort
  ORDER BY cohort
  """,
  [({"users": [(1, "Ava Moss", "BR", "2024-01-05"), (2, "Bilal Cruz", "CA", "2024-01-30"), (3, "Chen Ito", "DE", "2024-02-14")],
     "logins": [(1, "2024-02-01"), (1, "2024-02-09"), (2, "2024-01-31"), (2, "2024-03-02"), (3, "2024-03-15")]},
    "Ava (January) logged in during February, so she's retained. Bilal logged in on January 31 and in March, but not in February. Chen (February) came back in March.")],
  lambda rng, n, k: app(rng, n * 2, k, days=150),
  ordered=True,
  wrong=["SELECT strftime('%Y-%m', u.signed_up) AS cohort, COUNT(*) AS users, SUM(EXISTS (SELECT 1 FROM logins l WHERE l.user_id = u.id AND l.login_on > u.signed_up AND l.login_on <= date(u.signed_up, '+30 days'))) AS retained FROM users u GROUP BY cohort ORDER BY cohort",
         "SELECT strftime('%Y-%m', u.signed_up) AS cohort, COUNT(*) AS users, COUNT(l.user_id) AS retained FROM users u LEFT JOIN logins l ON l.user_id = u.id AND strftime('%Y-%m', l.login_on) = strftime('%Y-%m', u.signed_up, 'start of month', '+1 month') GROUP BY cohort ORDER BY cohort"],
  notes="`strftime('%Y-%m', '2024-01-30', 'start of month', '+1 month')` gives `'2024-02'`. Adding a month to January 30 directly would overflow into March.")

STATUS_LOG = T("status_log", ("order_id", "INTEGER"), ("status", "TEXT"), ("changed_at", "TEXT"))


def status_gen(rng, n, k):
    rows = []
    for o in range(1, n + 2):
        t = rng.randint(0, 300)
        steps = ["placed", "packed", "shipped", "delivered"]
        stop = rng.randint(1, 4)
        if rng.random() < 0.2:
            steps = ["placed", "cancelled"]
            stop = 2
        for s in steps[:stop]:
            rows.append((o, s, f"2024-06-{1 + t // 1440:02d} {t % 1440 // 60:02d}:{t % 60:02d}"))
            t += rng.randint(5, 600)
    rng.shuffle(rows)
    return {"status_log": rows}

P("current-status", "Current Status", "reporting", "dedup", "medium",
  """
  Every change to an order's status is logged in `status_log`. An order's **current** status is its most recent entry.
  No order has two entries at the same time.

  Return `order_id` and `status` (its current status) for every order in the log, in any order.
  """,
  [STATUS_LOG],
  """
  SELECT order_id, status
  FROM (SELECT order_id, status, ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY changed_at DESC) AS rn FROM status_log)
  WHERE rn = 1
  """,
  [({"status_log": [(7, "packed", "2024-06-01 10:00"), (7, "placed", "2024-06-01 09:00"), (8, "placed", "2024-06-01 09:30"),
                    (7, "shipped", "2024-06-02 08:15"), (8, "cancelled", "2024-06-01 09:45")]},
    "Order 7 was placed, packed, then shipped: it's shipped now. Order 8 was cancelled a quarter of an hour after it was placed.")],
  status_gen,
  wrong=["SELECT order_id, MAX(status) AS status FROM status_log GROUP BY order_id",
         "SELECT order_id, status FROM (SELECT order_id, status, ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY changed_at) AS rn FROM status_log) WHERE rn = 1"])

done()
