"""Filling Foundations and Core up to their planned counts."""
import _common  # noqa: F401
from _common import only
from _examples import EMP_EX, SCHOOL_EX, SHOP_EX, STAFF_EX
from author import P, T, day, done, maybe, names
from worlds import (COURSES, CUSTOMERS, DEPARTMENTS, EMPLOYEES, ENROLLMENTS, ORDER_ITEMS, ORDERS, PRODUCTS, STUDENTS,
                    school, shop, staff, ties)

ex = lambda data, *tables: only(data, *tables)  # noqa: E731

# --- Foundations -----------------------------------------------------------------------------

CART = T("cart_lines", ("id", "INTEGER", "pk"), ("item", "TEXT"), ("unit_price", "REAL"), ("quantity", "INTEGER"), ("discount_pct", "INTEGER"))
ITEMS = ["Teapot", "Whisk", "Seeds", "Comic", "Lamp", "Kite", "Drum", "Atlas", "Rake", "Chess"]


def cart_gen(rng, n, k):
    return {"cart_lines": [(i + 1, rng.choice(ITEMS), round(rng.uniform(1, 60), 2), rng.randint(1, 6), rng.choice([0, 5, 10, 15, 25, 50])) for i in range(n)]}

P("line-totals", "Line Totals", "select-filter", "pick-columns", "easy",
  """
  Each row of `cart_lines` is one item in a shopping cart, with a percentage discount (0 to 100).

  Return each line's `item` and `line_total`: `unit_price × quantity`, minus the discount, rounded to 2 decimal places.
  Any order.
  """,
  [CART],
  "SELECT item, ROUND(unit_price * quantity * (100 - discount_pct) / 100.0, 2) AS line_total FROM cart_lines",
  [({"cart_lines": [(1, "Teapot", 18.0, 2, 10), (2, "Whisk", 6.5, 3, 0), (3, "Seeds", 2.25, 4, 25)]},
    "Two teapots cost 36.00; 10% off leaves 32.40. Four packs of seeds cost 9.00; 25% off leaves 6.75.")],
  cart_gen,
  wrong=["SELECT item, ROUND(unit_price * quantity * ((100 - discount_pct) / 100), 2) AS line_total FROM cart_lines",
         "SELECT item, ROUND(unit_price * quantity - discount_pct, 2) AS line_total FROM cart_lines"],
  notes="`(100 - 10) / 100` is `0` in SQLite (whole-number division). Multiply first, or divide by `100.0`.")

OUT_EX = {"employees": EMP_EX["employees"] + [(6, "Fern Lund", 1, 1, 98000, "2021-09-01")]}

P("pay-outside-the-band", "Pay Outside the Band", "select-filter", "where-conditions", "easy",
  """
  HR is reviewing people hired in **2020 or 2021** whose salary falls **outside** the usual 60,000–90,000 band (the
  band includes both ends).

  Return `name`, `salary` and `hired_on` for those employees, in any order.
  """,
  [EMPLOYEES],
  "SELECT name, salary, hired_on FROM employees WHERE hired_on BETWEEN '2020-01-01' AND '2021-12-31' AND salary NOT BETWEEN 60000 AND 90000",
  [(OUT_EX, "Fern (hired 2021, 98,000) is outside the band. Bilal and Chen were hired in that window but earn inside it; Chen's 60,000 counts as inside.")],
  lambda rng, n, k: only(staff(rng, n, k), "employees") if not ties(k) else {"employees": [
      (i + 1, nm, 1, None, rng.choice([59999, 60000, 90000, 90001]), day(rng.randint(0, 1200), (2019, 6, 1))) for i, nm in enumerate(names(rng, n))]},
  wrong=["SELECT name, salary, hired_on FROM employees WHERE hired_on LIKE '2020%' OR hired_on LIKE '2021%' AND salary NOT BETWEEN 60000 AND 90000",
         "SELECT name, salary, hired_on FROM employees WHERE hired_on BETWEEN '2020-01-01' AND '2021-12-31' AND (salary < 60000 OR salary >= 90000)"])

P("no-department-last", "No Department Last", "sort-limit", "order-by", "easy",
  """
  List employees by `dept_id` from smallest to largest, with the people who have **no department at the end**. Within
  each group, order by `name`.

  Return `name` and `dept_id`.
  """,
  [EMPLOYEES],
  "SELECT name, dept_id FROM employees ORDER BY dept_id IS NULL, dept_id, name",
  [(EMP_EX, "Departments 1 and 2 come first, each sorted by name. Dara has no department, so she goes last.")],
  lambda rng, n, k: only(staff(rng, n, 1), "employees"),
  ordered=True,
  wrong=["SELECT name, dept_id FROM employees ORDER BY dept_id, name",
         "SELECT name, dept_id FROM employees ORDER BY dept_id DESC, name"],
  notes="SQLite puts NULLs first when sorting from small to large. `dept_id IS NULL` is 0 or 1, so sorting by it first moves the NULLs to the end. (`ORDER BY dept_id NULLS LAST` also works.)")

P("catalogue-at-a-glance", "Catalogue at a Glance", "aggregation", "aggregate-functions", "easy",
  """
  Summarise the catalogue in one row:

  - `products`: how many products there are
  - `categories`: how many **different** categories
  - `cheapest` and `priciest`: the lowest and highest price
  - `avg_price`: the average price, rounded to 2 decimal places
  """,
  [PRODUCTS],
  "SELECT COUNT(*) AS products, COUNT(DISTINCT category) AS categories, MIN(price) AS cheapest, MAX(price) AS priciest, ROUND(AVG(price), 2) AS avg_price FROM products",
  [(ex(SHOP_EX, "products"), "Four products in three categories (two are Books). The average is 51.00 / 4 = 12.75.")],
  lambda rng, n, k: only(shop(rng, n * 2, k), "products"),
  wrong=["SELECT COUNT(*) AS products, COUNT(category) AS categories, MIN(price) AS cheapest, MAX(price) AS priciest, ROUND(AVG(price), 2) AS avg_price FROM products",
         "SELECT COUNT(*) AS products, COUNT(DISTINCT category) AS categories, MIN(price) AS cheapest, MAX(price) AS priciest, ROUND(AVG(DISTINCT price), 2) AS avg_price FROM products"])

P("averages-with-gaps", "Averages with Gaps", "aggregation", "aggregate-functions", "medium",
  """
  Some enrollments have no `score` yet (NULL). Report, in one row:

  - `enrollments`: all enrollments
  - `marked`: how many have a score
  - `avg_marked`: the average of the scores that exist, rounded to 2 decimal places
  - `avg_all`: the average if every missing score counted as 0, rounded to 2 decimal places
  """,
  [ENROLLMENTS],
  "SELECT COUNT(*) AS enrollments, COUNT(score) AS marked, ROUND(AVG(score), 2) AS avg_marked, ROUND(AVG(COALESCE(score, 0)), 2) AS avg_all FROM enrollments",
  [(ex(SCHOOL_EX, "enrollments"), "Two of the three enrollments are marked: 88 and 72 average 80.00. Counting the missing one as 0 gives 160 / 3 = 53.33.")],
  lambda rng, n, k: only(school(rng, n, 1 if k % 2 else k), "enrollments"),
  wrong=["SELECT COUNT(*) AS enrollments, COUNT(score) AS marked, ROUND(AVG(score), 2) AS avg_marked, ROUND(AVG(score), 2) AS avg_all FROM enrollments",
         "SELECT COUNT(*) AS enrollments, COUNT(*) AS marked, ROUND(AVG(score), 2) AS avg_marked, ROUND(SUM(score) * 1.0 / COUNT(*), 2) AS avg_all FROM enrollments"],
  notes="Aggregates like `AVG` skip NULLs: the average is over the marked rows only.")

P("customers-per-city", "Customers per City", "aggregation", "group-by", "easy",
  """
  For each city, return `city`, `customers` (how many customers live there) and `first_joined` (the earliest
  `joined_on` among them). Order by `customers` from most to fewest, then by `city`.
  """,
  [CUSTOMERS],
  "SELECT city, COUNT(*) AS customers, MIN(joined_on) AS first_joined FROM customers GROUP BY city ORDER BY customers DESC, city",
  [(ex(SHOP_EX, "customers"), "Osaka has two customers; Omar joined first, on 2023-02-01. Denver and Lisbon have one each.")],
  lambda rng, n, k: only(shop(rng, n * 2, k), "customers"),
  ordered=True,
  wrong=["SELECT city, COUNT(*) AS customers, MAX(joined_on) AS first_joined FROM customers GROUP BY city ORDER BY customers DESC, city",
         "SELECT city, COUNT(*) AS customers, MIN(joined_on) AS first_joined FROM customers GROUP BY city ORDER BY city"])

P("course-averages", "Course Averages", "aggregation", "group-by", "easy",
  """
  For every course with enrollments, return `course_id`, `students` (how many are enrolled) and `avg_score` (the
  average of the scores that exist, rounded to 1 decimal place; NULL if nobody is marked yet). Any order.
  """,
  [ENROLLMENTS],
  "SELECT course_id, COUNT(*) AS students, ROUND(AVG(score), 1) AS avg_score FROM enrollments GROUP BY course_id",
  [({"enrollments": [(1, 1, 88), (2, 1, None), (1, 2, 72), (3, 3, None)]},
    "Course 1 has two students but only one score, so its average is 88.0. Nobody in course 3 is marked yet.")],
  lambda rng, n, k: only(school(rng, n, 1 if k % 2 else k), "enrollments"),
  wrong=["SELECT course_id, COUNT(score) AS students, ROUND(AVG(score), 1) AS avg_score FROM enrollments GROUP BY course_id",
         "SELECT course_id, COUNT(*) AS students, ROUND(AVG(COALESCE(score, 0)), 1) AS avg_score FROM enrollments GROUP BY course_id"])

SIDES = T("triangles", ("id", "INTEGER", "pk"), ("a", "INTEGER"), ("b", "INTEGER"), ("c", "INTEGER"))


def sides_gen(rng, n, k):
    rows = []
    for i in range(n + 2):
        a, b = rng.randint(1, 6), rng.randint(1, 6)
        c = rng.choice([a, b, a + b, abs(a - b) or 1, rng.randint(1, 9)])
        rows.append((i + 1, *rng.sample([a, b, c], 3)))
    return {"triangles": rows}

P("triangle-check", "Triangle Check", "conditional", "case-when", "medium",
  """
  Each row holds three side lengths. Three sides make a triangle only if **every two sides together are longer than the
  third**. Label each row:

  - `'not a triangle'` if the sides can't make one
  - `'equilateral'` if all three sides are equal
  - `'isosceles'` if exactly two are equal
  - `'scalene'` if all three differ

  Return `id` and `kind`, in any order.
  """,
  [SIDES],
  """
  SELECT id,
         CASE WHEN a + b <= c OR a + c <= b OR b + c <= a THEN 'not a triangle'
              WHEN a = b AND b = c THEN 'equilateral'
              WHEN a = b OR b = c OR a = c THEN 'isosceles'
              ELSE 'scalene' END AS kind
  FROM triangles
  """,
  [({"triangles": [(1, 3, 3, 3), (2, 3, 4, 5), (3, 2, 2, 5), (4, 5, 5, 8), (5, 1, 2, 3)]},
    "Row 3 has two equal sides, but 2 + 2 isn't more than 5, so it isn't a triangle. In row 5, 1 + 2 only equals 3: still not a triangle.")],
  sides_gen,
  wrong=["SELECT id, CASE WHEN a = b AND b = c THEN 'equilateral' WHEN a = b OR b = c OR a = c THEN 'isosceles' WHEN a + b <= c OR a + c <= b OR b + c <= a THEN 'not a triangle' ELSE 'scalene' END AS kind FROM triangles",
         "SELECT id, CASE WHEN a + b < c OR a + c < b OR b + c < a THEN 'not a triangle' WHEN a = b AND b = c THEN 'equilateral' WHEN a = b OR b = c OR a = c THEN 'isosceles' ELSE 'scalene' END AS kind FROM triangles"],
  notes="`CASE` takes the first `WHEN` that matches, so the order of the checks matters.")

SHIPMENTS = T("shipments", ("order_id", "INTEGER", "pk"), ("ordered_on", "TEXT"), ("shipped_on", "TEXT"))


def ship_gen(rng, n, k):
    rows = []
    for i in range(n + 1):
        start = rng.randint(0, 120)
        rows.append((i + 1, day(start), maybe(rng, 0.25, day(start + rng.randint(0, 5)))))
    return {"shipments": rows}

P("shipping-speed", "Shipping Speed", "conditional", "case-when", "easy",
  """
  Label every shipment by how long it took from `ordered_on` to `shipped_on`:

  - `'pending'` if it hasn't shipped (`shipped_on` is NULL)
  - `'same day'` if it shipped the day it was ordered
  - `'fast'` if it took 1 or 2 days
  - `'slow'` if it took 3 days or more

  Return `order_id` and `speed`, in any order.
  """,
  [SHIPMENTS],
  """
  SELECT order_id,
         CASE WHEN shipped_on IS NULL THEN 'pending'
              WHEN julianday(shipped_on) - julianday(ordered_on) = 0 THEN 'same day'
              WHEN julianday(shipped_on) - julianday(ordered_on) <= 2 THEN 'fast'
              ELSE 'slow' END AS speed
  FROM shipments
  """,
  [({"shipments": [(1, "2024-01-30", "2024-01-30"), (2, "2024-02-01", "2024-02-03"), (3, "2024-02-01", None), (4, "2024-02-05", "2024-02-09")]},
    "Order 2 took 2 days (fast), order 4 took 4 (slow), and order 3 hasn't shipped yet.")],
  ship_gen,
  wrong=["SELECT order_id, CASE WHEN julianday(shipped_on) - julianday(ordered_on) = 0 THEN 'same day' WHEN julianday(shipped_on) - julianday(ordered_on) <= 2 THEN 'fast' ELSE 'slow' END AS speed FROM shipments",
         "SELECT order_id, CASE WHEN shipped_on IS NULL THEN 'pending' WHEN julianday(shipped_on) - julianday(ordered_on) = 0 THEN 'same day' WHEN julianday(shipped_on) - julianday(ordered_on) <= 3 THEN 'fast' ELSE 'slow' END AS speed FROM shipments"],
  notes="A comparison with NULL is never true, so a row with no `shipped_on` falls through to `ELSE` unless you check for NULL first.")

P("pass-rates", "Pass Rates", "conditional", "conditional-aggregation", "medium",
  """
  A score of **50 or more** passes. For every course with enrollments, return:

  - `course_id`
  - `passed`, `failed` and `unmarked` (NULL score) counts
  - `pass_rate`: passed as a percentage of the **marked** enrollments, rounded to 1 decimal place, or NULL when none
    are marked

  Any order.
  """,
  [ENROLLMENTS],
  """
  SELECT course_id,
         SUM(CASE WHEN score >= 50 THEN 1 ELSE 0 END) AS passed,
         SUM(CASE WHEN score < 50 THEN 1 ELSE 0 END) AS failed,
         SUM(CASE WHEN score IS NULL THEN 1 ELSE 0 END) AS unmarked,
         ROUND(100.0 * SUM(CASE WHEN score >= 50 THEN 1 ELSE 0 END) / NULLIF(COUNT(score), 0), 1) AS pass_rate
  FROM enrollments
  GROUP BY course_id
  """,
  [({"enrollments": [(1, 1, 88), (2, 1, 40), (3, 1, None), (1, 2, None)]},
    "Course 1 has one pass, one fail and one unmarked: 1 of 2 marked passed, 50.0%. Course 2 has nothing marked, so its rate is NULL.")],
  lambda rng, n, k: only(school(rng, n, 1 if k % 2 else 2), "enrollments"),
  wrong=["SELECT course_id, SUM(CASE WHEN score >= 50 THEN 1 ELSE 0 END) AS passed, SUM(CASE WHEN score < 50 THEN 1 ELSE 0 END) AS failed, SUM(CASE WHEN score IS NULL THEN 1 ELSE 0 END) AS unmarked, ROUND(100.0 * SUM(CASE WHEN score >= 50 THEN 1 ELSE 0 END) / COUNT(*), 1) AS pass_rate FROM enrollments GROUP BY course_id",
         "SELECT course_id, SUM(CASE WHEN score >= 50 THEN 1 ELSE 0 END) AS passed, SUM(CASE WHEN score >= 50 THEN 0 ELSE 1 END) AS failed, SUM(CASE WHEN score IS NULL THEN 1 ELSE 0 END) AS unmarked, ROUND(100.0 * SUM(CASE WHEN score >= 50 THEN 1 ELSE 0 END) / NULLIF(COUNT(score), 0), 1) AS pass_rate FROM enrollments GROUP BY course_id"],
  notes="`NULLIF(x, 0)` is NULL when `x` is 0, and dividing by NULL gives NULL instead of an error.")

# --- Core ------------------------------------------------------------------------------------------

P("course-roster", "Course Roster", "joins", "inner-join", "easy",
  """
  Print every course's roster: one row per enrollment with the course `title` and the student's `name`. Order by
  `title`, then `name`.
  """,
  [STUDENTS, COURSES, ENROLLMENTS],
  "SELECT c.title, s.name FROM enrollments e JOIN courses c ON c.id = e.course_id JOIN students s ON s.id = e.student_id ORDER BY c.title, s.name",
  [(SCHOOL_EX, "Algebra has Ava and Bilal; Biology has Ava. Nobody takes Drawing, and Chen takes nothing, so neither appears.")],
  lambda rng, n, k: school(rng, n, k),
  ordered=True,
  wrong=["SELECT c.title, s.name FROM enrollments e JOIN courses c ON c.id = e.student_id JOIN students s ON s.id = e.course_id ORDER BY c.title, s.name",
         "SELECT c.title, s.name FROM enrollments e JOIN courses c ON c.id = e.course_id JOIN students s ON s.id = e.student_id ORDER BY s.name, c.title"])

P("big-ticket-items", "Big-ticket Items", "joins", "inner-join", "easy",
  """
  Find order lines for products that cost **20 or more**.

  Return `order_id`, the product's `name` and the `quantity`, in any order.
  """,
  [PRODUCTS, ORDER_ITEMS],
  "SELECT i.order_id, p.name, i.quantity FROM order_items i JOIN products p ON p.id = i.product_id WHERE p.price >= 20",
  [(ex(SHOP_EX, "products", "order_items"), "Only the Kettle (24.50) costs 20 or more, and it appears once: two of them in order 1.")],
  lambda rng, n, k: only(shop(rng, n, k), "products", "order_items"),
  wrong=["SELECT i.order_id, p.name, i.quantity FROM order_items i JOIN products p ON p.id = i.product_id WHERE p.price > 20",
         "SELECT i.order_id, p.name, i.quantity FROM order_items i JOIN products p ON p.id = i.order_id WHERE p.price >= 20"])

P("courses-per-student", "Courses per Student", "joins", "left-join", "easy",
  """
  Return every student's `name` and `courses` (how many courses they're enrolled in, `0` if none). Order by `courses`
  from most to fewest, then by `name`.
  """,
  [STUDENTS, ENROLLMENTS],
  "SELECT s.name, COUNT(e.course_id) AS courses FROM students s LEFT JOIN enrollments e ON e.student_id = s.id GROUP BY s.id, s.name ORDER BY courses DESC, s.name",
  [(ex(SCHOOL_EX, "students", "enrollments"), "Ava takes two courses and Bilal one. Chen takes none, so he shows 0.")],
  lambda rng, n, k: only(school(rng, n, k), "students", "enrollments"),
  ordered=True,
  wrong=["SELECT s.name, COUNT(*) AS courses FROM students s LEFT JOIN enrollments e ON e.student_id = s.id GROUP BY s.id, s.name ORDER BY courses DESC, s.name",
         "SELECT s.name, COUNT(e.course_id) AS courses FROM students s JOIN enrollments e ON e.student_id = s.id GROUP BY s.id, s.name ORDER BY courses DESC, s.name"])

P("last-order-date", "Last Order Date", "joins", "left-join", "medium",
  """
  Return every customer's `name` and `last_order`: the date of their most recent order of any status, or NULL if they
  never ordered. Any order.
  """,
  [CUSTOMERS, ORDERS],
  "SELECT c.name, MAX(o.ordered_on) AS last_order FROM customers c LEFT JOIN orders o ON o.customer_id = c.id GROUP BY c.id, c.name",
  [(ex(SHOP_EX, "customers", "orders"), "Omar ordered on January 3 and February 10, so his last order is 2024-02-10. Uma never ordered.")],
  lambda rng, n, k: only(shop(rng, n, k), "customers", "orders"),
  wrong=["SELECT c.name, MAX(o.ordered_on) AS last_order FROM customers c JOIN orders o ON o.customer_id = c.id GROUP BY c.id, c.name",
         "SELECT c.name, MIN(o.ordered_on) AS last_order FROM customers c LEFT JOIN orders o ON o.customer_id = c.id GROUP BY c.id, c.name"])

P("units-sold", "Units Sold", "joins", "left-join", "medium",
  """
  Return every product's `name` and `units`: the total quantity in **delivered** orders, `0` if it has none. Order by
  `units` from most to least, then by `name`.
  """,
  [PRODUCTS, ORDERS, ORDER_ITEMS],
  """
  SELECT p.name, COALESCE(SUM(CASE WHEN o.status = 'delivered' THEN i.quantity END), 0) AS units
  FROM products p
  LEFT JOIN order_items i ON i.product_id = p.id
  LEFT JOIN orders o ON o.id = i.order_id
  GROUP BY p.id, p.name
  ORDER BY units DESC, p.name
  """,
  [(ex(SHOP_EX, "products", "orders", "order_items"), "Delivered orders 1 and 3 hold two Kettles, a Novel and two Comics. The Kite only appears in orders that weren't delivered, so it shows 0.")],
  lambda rng, n, k: only(shop(rng, n, k), "products", "orders", "order_items"),
  ordered=True,
  wrong=["SELECT p.name, COALESCE(SUM(i.quantity), 0) AS units FROM products p LEFT JOIN order_items i ON i.product_id = p.id LEFT JOIN orders o ON o.id = i.order_id WHERE o.status = 'delivered' GROUP BY p.id, p.name ORDER BY units DESC, p.name",
         "SELECT p.name, COALESCE(SUM(i.quantity), 0) AS units FROM products p LEFT JOIN order_items i ON i.product_id = p.id GROUP BY p.id, p.name ORDER BY units DESC, p.name"])

P("credit-load", "Credit Load", "joins", "multi-join", "medium",
  """
  A student's credit load is the sum of `credits` of the courses they're enrolled in.

  For every student enrolled in at least one course, return `name` and `credits`. Order by `credits` from most to
  least, then by `name`.
  """,
  [STUDENTS, COURSES, ENROLLMENTS],
  "SELECT s.name, SUM(c.credits) AS credits FROM students s JOIN enrollments e ON e.student_id = s.id JOIN courses c ON c.id = e.course_id GROUP BY s.id, s.name ORDER BY credits DESC, s.name",
  [(SCHOOL_EX, "Ava takes Algebra (3) and Biology (4): 7 credits. Bilal takes Algebra: 3.")],
  lambda rng, n, k: school(rng, n, k),
  ordered=True,
  wrong=["SELECT s.name, COUNT(*) AS credits FROM students s JOIN enrollments e ON e.student_id = s.id JOIN courses c ON c.id = e.course_id GROUP BY s.id, s.name ORDER BY credits DESC, s.name",
         "SELECT s.name, SUM(c.credits) AS credits FROM students s JOIN enrollments e ON e.student_id = s.id JOIN courses c ON c.id = e.student_id GROUP BY s.id, s.name ORDER BY credits DESC, s.name"])

SIZES_T = T("sizes", ("size", "TEXT"))
COLOURS_T = T("colours", ("colour", "TEXT"))
STOCK_T = T("stock", ("size", "TEXT"), ("colour", "TEXT"), ("qty", "INTEGER"))


def stock_gen(rng, n, k):
    sizes = rng.sample(["XS", "S", "M", "L", "XL"], rng.randint(1, 5))
    colours = rng.sample(["Blue", "Green", "Grey", "Red", "Sand", "White"], rng.randint(1, min(6, n + 1)))
    stock = [(s, c, rng.randint(0, 9)) for s in sizes for c in colours if rng.random() < 0.5]
    return {"sizes": [(s,) for s in sizes], "colours": [(c,) for c in colours], "stock": stock}

P("stock-grid", "Stock Grid", "joins", "cross-join", "medium",
  """
  A clothing shop sells every `size` in every `colour`, but `stock` only has rows for combinations that were ever
  stocked.

  Return a full grid: every size with every colour, as `size`, `colour` and `qty` (`0` where `stock` has no row).
  Order by `size`, then `colour` (alphabetically).
  """,
  [SIZES_T, COLOURS_T, STOCK_T],
  """
  SELECT s.size, c.colour, COALESCE(t.qty, 0) AS qty
  FROM sizes s
  CROSS JOIN colours c
  LEFT JOIN stock t ON t.size = s.size AND t.colour = c.colour
  ORDER BY s.size, c.colour
  """,
  [({"sizes": [("S",), ("M",)], "colours": [("Red",), ("Blue",)], "stock": [("S", "Red", 4), ("M", "Blue", 0)]},
    "2 sizes × 2 colours = 4 rows. Only small red has stock; medium blue has a row, but its quantity is 0 too.")],
  stock_gen,
  ordered=True,
  wrong=["SELECT t.size, t.colour, t.qty FROM stock t ORDER BY t.size, t.colour",
         "SELECT s.size, c.colour, t.qty FROM sizes s CROSS JOIN colours c LEFT JOIN stock t ON t.size = s.size AND t.colour = c.colour ORDER BY s.size, c.colour"],
  sizes=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])


def newest_gen(rng, n, k):
    return {"customers": [(i + 1, nm, "Osaka", day(rng.randint(0, 3 if ties(k) else 200), (2023, 1, 1))) for i, nm in enumerate(names(rng, n))]}

P("newest-customers", "Newest Customers", "subqueries", "scalar-subquery", "easy",
  """
  Return the `id` and `name` of every customer who joined on the **most recent** `joined_on` date. Several customers
  can share that date. Any order.
  """,
  [CUSTOMERS],
  "SELECT id, name FROM customers WHERE joined_on = (SELECT MAX(joined_on) FROM customers)",
  [(ex(SHOP_EX, "customers"), "The latest join date is 2023-08-03, and only Uma joined then.")],
  newest_gen,
  wrong=["SELECT id, name FROM customers ORDER BY joined_on DESC LIMIT 1",
         "SELECT id, name FROM customers WHERE joined_on = (SELECT MIN(joined_on) FROM customers)"])

P("bigger-than-average-order", "Bigger Than the Average Order", "subqueries", "scalar-subquery", "medium",
  """
  An order's size is the total `quantity` of its items. Find the orders whose size is **larger than the average order
  size**.

  Return `order_id` and `items` (its size), ordered by `order_id`.
  """,
  [ORDER_ITEMS],
  """
  WITH sizes AS (
    SELECT order_id, SUM(quantity) AS items FROM order_items GROUP BY order_id
  )
  SELECT order_id, items FROM sizes
  WHERE items > (SELECT AVG(items) FROM sizes)
  ORDER BY order_id
  """,
  [(ex(SHOP_EX, "order_items"), "Orders 1 and 2 hold 3 items each, orders 3 and 4 hold 2: the average order has 2.5 items.")],
  lambda rng, n, k: only(shop(rng, n, k), "order_items"),
  ordered=True,
  wrong=["SELECT order_id, SUM(quantity) AS items FROM order_items GROUP BY order_id HAVING SUM(quantity) > (SELECT AVG(quantity) FROM order_items) ORDER BY order_id",
         "WITH sizes AS (SELECT order_id, SUM(quantity) AS items FROM order_items GROUP BY order_id) SELECT order_id, items FROM sizes WHERE items >= (SELECT AVG(items) FROM sizes) ORDER BY order_id"],
  sizes=[2, 3, 4, 6, 8, 10, 14, 20, 30, 45, 70, 120])

P("ever-cancelled", "Ever Cancelled", "subqueries", "in-exists", "easy",
  """
  Return the `name` of every customer who has cancelled **at least one** order, each name once, in any order.
  """,
  [CUSTOMERS, ORDERS],
  "SELECT name FROM customers WHERE id IN (SELECT customer_id FROM orders WHERE status = 'cancelled')",
  [(ex(SHOP_EX, "customers", "orders"), "Only Priya's order was cancelled.")],
  lambda rng, n, k: only(shop(rng, n * 2 + 3, k), "customers", "orders"),
  wrong=["SELECT c.name FROM customers c JOIN orders o ON o.customer_id = c.id WHERE o.status = 'cancelled'",
         "SELECT name FROM customers WHERE id IN (SELECT customer_id FROM orders WHERE status <> 'cancelled')"])

P("never-cancelled", "Never Cancelled", "subqueries", "in-exists", "medium",
  """
  Return the `name` of every customer who **has placed orders** but has **never cancelled** one, in any order.
  """,
  [CUSTOMERS, ORDERS],
  """
  SELECT c.name FROM customers c
  WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id)
    AND NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id AND o.status = 'cancelled')
  """,
  [(ex(SHOP_EX, "customers", "orders"), "Omar and Elif have orders and none were cancelled. Priya cancelled hers, and Uma has never ordered.")],
  lambda rng, n, k: only(shop(rng, n, k), "customers", "orders"),
  wrong=["SELECT c.name FROM customers c WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id AND o.status = 'cancelled')",
         "SELECT DISTINCT c.name FROM customers c JOIN orders o ON o.customer_id = c.id WHERE o.status <> 'cancelled'"])

P("newest-hire-per-department", "Newest Hire per Department", "subqueries", "correlated", "medium",
  """
  For each department, find the person hired **most recently**. If several were hired on that same day, list them all.

  Return the `department` name, the employee's `name` and `hired_on`, in any order. Employees without a department are
  left out.
  """,
  [DEPARTMENTS, EMPLOYEES],
  """
  SELECT d.name AS department, e.name, e.hired_on
  FROM employees e
  JOIN departments d ON d.id = e.dept_id
  WHERE e.hired_on = (SELECT MAX(x.hired_on) FROM employees x WHERE x.dept_id = e.dept_id)
  """,
  [(STAFF_EX, "Chen is Design's newest hire (2021) and Elif is Sales' (2022). Legal has nobody.")],
  lambda rng, n, k: (lambda d: {**d, "employees": [r[:5] + (day(rng.randint(0, 3), (2022, 5, 1)),) for r in d["employees"]] if ties(k) else d["employees"]})(staff(rng, n, k)),
  wrong=["SELECT d.name AS department, e.name, e.hired_on FROM employees e JOIN departments d ON d.id = e.dept_id WHERE e.hired_on = (SELECT MAX(hired_on) FROM employees)",
         "SELECT d.name AS department, e.name, e.hired_on FROM employees e JOIN departments d ON d.id = e.dept_id WHERE e.hired_on = (SELECT MIN(x.hired_on) FROM employees x WHERE x.dept_id = e.dept_id)"])

P("repeat-buyers", "Repeat Buyers", "ctes", "step-ctes", "medium",
  """
  A **buyer** is a customer with at least one order (any status); a **repeat buyer** has at least two.

  Return one row: `buyers`, `repeat_buyers`, and `repeat_pct` (repeat buyers as a percentage of buyers, rounded to 1
  decimal place).
  """,
  [ORDERS],
  """
  WITH per_customer AS (
    SELECT customer_id, COUNT(*) AS orders FROM orders GROUP BY customer_id
  )
  SELECT COUNT(*) AS buyers,
         SUM(CASE WHEN orders >= 2 THEN 1 ELSE 0 END) AS repeat_buyers,
         ROUND(100.0 * SUM(CASE WHEN orders >= 2 THEN 1 ELSE 0 END) / COUNT(*), 1) AS repeat_pct
  FROM per_customer
  """,
  [(ex(SHOP_EX, "orders"), "Three customers have ordered, and only Omar has ordered twice: 1 of 3 is 33.3%.")],
  lambda rng, n, k: only(shop(rng, n, k), "orders"),
  wrong=["WITH per_customer AS (SELECT customer_id, COUNT(*) AS orders FROM orders GROUP BY customer_id) SELECT COUNT(*) AS buyers, SUM(CASE WHEN orders >= 2 THEN 1 ELSE 0 END) AS repeat_buyers, ROUND(100 * SUM(CASE WHEN orders >= 2 THEN 1 ELSE 0 END) / COUNT(*), 1) AS repeat_pct FROM per_customer",
         "WITH per_customer AS (SELECT customer_id, COUNT(*) AS orders FROM orders GROUP BY customer_id) SELECT COUNT(*) AS buyers, SUM(CASE WHEN orders > 2 THEN 1 ELSE 0 END) AS repeat_buyers, ROUND(100.0 * SUM(CASE WHEN orders > 2 THEN 1 ELSE 0 END) / COUNT(*), 1) AS repeat_pct FROM per_customer"])

PHONES = T("phones", ("id", "INTEGER", "pk"), ("phone", "TEXT"))


def phones_gen(rng, n, k):
    rows = []
    for i in range(n):
        a, b, c = rng.randint(200, 999), rng.randint(0, 999), rng.randint(0, 9999)
        fmt = rng.choice(["({a}) {b:03d}-{c:04d}", "{a}.{b:03d}.{c:04d}", "{a} {b:03d} {c:04d}", "{a}-{b:03d}-{c:04d}", "{a}{b:03d}{c:04d}"])
        rows.append((i + 1, fmt.format(a=a, b=b, c=c)))
    return {"phones": rows}

P("phone-digits", "Phone Digits", "strings-dates", "string-functions", "medium",
  """
  Phone numbers were typed in different styles: `(555) 014-2233`, `555.014.2233`, `555 014 2233`, `555-014-2233`.
  Clean them up so only the digits are left.

  Return `id` and `digits`, in any order.
  """,
  [PHONES],
  "SELECT id, REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(phone, '(', ''), ')', ''), '-', ''), '.', ''), ' ', '') AS digits FROM phones",
  [({"phones": [(1, "(555) 014-2233"), (2, "555.014.2233"), (3, "555 014 2233")]}, "All three become `5550142233`.")],
  phones_gen,
  wrong=["SELECT id, REPLACE(REPLACE(REPLACE(REPLACE(phone, '(', ''), ')', ''), '-', ''), '.', '') AS digits FROM phones",
         "SELECT id, REPLACE(REPLACE(REPLACE(phone, '-', ''), '.', ''), ' ', '') AS digits FROM phones"])


def tenure_gen(rng, n, k):
    if ties(k):  # hired close to the June 30 anniversary
        return {"employees": [(i + 1, nm, 1, None, 60000, f"{rng.randint(2016, 2024)}-{rng.choice(['06-28', '06-29', '06-30', '07-01', '07-02'])}") for i, nm in enumerate(names(rng, n))]}
    return {"employees": [(i + 1, nm, 1, None, 60000, day(rng.randint(0, 3600), (2015, 1, 1))) for i, nm in enumerate(names(rng, n))]}

P("years-of-service", "Years of Service", "strings-dates", "date-functions", "medium",
  """
  Count each employee's **completed** years of service as of **2025-06-30**: someone hired on 2020-07-15 has completed 4
  years (the 5th anniversary hasn't come yet), and someone hired on 2020-06-30 has completed 5.

  Return `name` and `years`, in any order.
  """,
  [EMPLOYEES],
  """
  SELECT name,
         (2025 - CAST(strftime('%Y', hired_on) AS INTEGER)) - (strftime('%m-%d', hired_on) > '06-30') AS years
  FROM employees
  """,
  [(EMP_EX, "Ava (2019-03-04) has passed her 6th anniversary. Bilal (2020-07-15) hasn't reached his 5th yet, so he has 4.")],
  tenure_gen,
  wrong=["SELECT name, 2025 - CAST(strftime('%Y', hired_on) AS INTEGER) AS years FROM employees",
         "SELECT name, CAST((julianday('2025-06-30') - julianday(hired_on)) / 365 AS INTEGER) AS years FROM employees"],
  notes="`strftime('%m-%d', d)` gives the month and day as text, like `'07-15'`, which compares correctly as text. A comparison is 1 when true and 0 when false.")

done()
