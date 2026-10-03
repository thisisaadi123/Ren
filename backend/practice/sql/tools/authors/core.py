"""Core: joins, set operations, subqueries, CTEs, strings and dates."""
import _common  # noqa: F401
from _common import only
from author import FIRST, P, T, day, done, maybe, names
from worlds import (COURSES, CUSTOMERS, DEPARTMENTS, EMPLOYEES, ENROLLMENTS, ORDER_ITEMS, ORDERS, PRODUCTS, STUDENTS,
                    school, shop, staff, ties)

STAFF_EX = {
    "departments": [(1, "Design", "Lisbon"), (2, "Sales", "Osaka"), (3, "Legal", "Denver")],
    "employees": [
        (1, "Ava Moss", 1, None, 96000, "2019-03-04"),
        (2, "Bilal Cruz", 2, 1, 61000, "2020-07-15"),
        (3, "Chen Ito", 1, 1, 60000, "2021-01-10"),
        (4, "Dara Kerr", None, 2, 125500, "2019-03-04"),
        (5, "Elif Park", 2, 2, 48000, "2022-11-30"),
    ],
}
SHOP_EX = {
    "customers": [(1, "Omar Fox", "Osaka", "2023-02-01"), (2, "Priya Nair", "Lisbon", "2023-05-12"),
                  (3, "Elif Gray", "Denver", "2023-01-20"), (4, "Uma Sato", "Osaka", "2023-08-03")],
    "products": [(1, "Kettle", "Kitchen", 24.5), (2, "Novel", "Books", 12.0), (3, "Kite", "Toys", 8.0), (4, "Comic", "Books", 6.5)],
    "orders": [(1, 1, "2024-01-03", "delivered"), (2, 2, "2024-01-04", "cancelled"),
               (3, 1, "2024-02-10", "delivered"), (4, 3, "2024-02-11", "shipped")],
    "order_items": [(1, 1, 2), (1, 2, 1), (2, 3, 3), (3, 4, 2), (4, 2, 1), (4, 3, 1)],
}
SCHOOL_EX = {
    "students": [(1, "Ava", 1), (2, "Bilal", 2), (3, "Chen", 1)],
    "courses": [(1, "Algebra", 3), (2, "Biology", 4), (3, "Drawing", 2)],
    "enrollments": [(1, 1, 88), (1, 2, None), (2, 1, 72)],
}
ex = lambda data, *tables: only(data, *tables)  # noqa: E731

# --- Joins ---------------------------------------------------------------------------------------

P("delivered-orders", "Who Got Their Order", "joins", "inner-join", "easy",
  """
  Support wants a list of delivered orders with the customer's name next to each one.

  Return `order_id`, the customer's `name` and `ordered_on` for every order whose status is `'delivered'`, in any order.
  """,
  [CUSTOMERS, ORDERS],
  "SELECT o.id AS order_id, c.name, o.ordered_on FROM orders o JOIN customers c ON c.id = o.customer_id WHERE o.status = 'delivered'",
  [(ex(SHOP_EX, "customers", "orders"), "Orders 1 and 3 were delivered, both to Omar. Order 2 was cancelled and order 4 is still shipping.")],
  lambda rng, n, k: only(shop(rng, n, k), "customers", "orders"),
  wrong=["SELECT o.id AS order_id, c.name, o.ordered_on FROM orders o JOIN customers c ON c.id = o.id WHERE o.status = 'delivered'",
         "SELECT o.id AS order_id, c.name, o.ordered_on FROM orders o JOIN customers c ON c.id = o.customer_id"])

P("department-directory", "Department Directory", "joins", "inner-join", "easy",
  """
  Print the staff directory: each employee next to their department's name.

  Return the employee's `name` and the `department` name, in any order. Employees without a department aren't listed.
  """,
  [DEPARTMENTS, EMPLOYEES],
  "SELECT e.name, d.name AS department FROM employees e JOIN departments d ON d.id = e.dept_id",
  [(STAFF_EX, "Dara has no department, so she isn't in the directory. Nobody works in Legal yet.")],
  lambda rng, n, k: staff(rng, n, k),
  wrong=["SELECT e.name, d.name AS department FROM employees e LEFT JOIN departments d ON d.id = e.dept_id",
         "SELECT e.name, d.name AS department FROM employees e JOIN departments d ON d.id = e.id"])

P("headcount-every-department", "Every Department's Headcount", "joins", "left-join", "medium",
  """
  Return every department with how many employees it has, **including departments with nobody in them**.

  Columns: the department's `name` and `headcount`. Order by `headcount` from largest to smallest, then by `name`.
  """,
  [DEPARTMENTS, EMPLOYEES],
  "SELECT d.name, COUNT(e.id) AS headcount FROM departments d LEFT JOIN employees e ON e.dept_id = d.id GROUP BY d.id, d.name ORDER BY headcount DESC, d.name",
  [(STAFF_EX, "Design and Sales have two people each. Legal has nobody, so it shows 0.")],
  lambda rng, n, k: staff(rng, n, k),
  ordered=True,
  wrong=["SELECT d.name, COUNT(*) AS headcount FROM departments d LEFT JOIN employees e ON e.dept_id = d.id GROUP BY d.id, d.name ORDER BY headcount DESC, d.name",
         "SELECT d.name, COUNT(e.id) AS headcount FROM departments d JOIN employees e ON e.dept_id = d.id GROUP BY d.id, d.name ORDER BY headcount DESC, d.name"],
  notes="`COUNT(*)` counts rows, and a department with no match still produces one row (full of NULLs). `COUNT(column)` skips NULLs.")

P("customers-without-orders", "Never Ordered", "joins", "anti-join", "easy",
  """
  Find the customers who signed up but have **never placed an order**.

  Return their `id` and `name`, in any order.
  """,
  [CUSTOMERS, ORDERS],
  "SELECT c.id, c.name FROM customers c LEFT JOIN orders o ON o.customer_id = c.id WHERE o.id IS NULL",
  [(ex(SHOP_EX, "customers", "orders"), "Uma is the only customer with no orders.")],
  lambda rng, n, k: only(shop(rng, n, k), "customers", "orders"),
  wrong=["SELECT c.id, c.name FROM customers c LEFT JOIN orders o ON o.customer_id = c.id WHERE o.id IS NOT NULL",
         "SELECT c.id, c.name FROM customers c WHERE c.id NOT IN (SELECT id FROM orders)"])

def empty_courses(rng, n, k):
    """A school where a few courses (usually) lost all their students."""
    d = only(school(rng, n, k), "courses", "enrollments")
    ids = [c[0] for c in d["courses"]]
    if k % 5:
        dropped = set(rng.sample(ids, max(1, len(ids) // 3)))
        d["enrollments"] = [e for e in d["enrollments"] if e[1] not in dropped]
    return d

P("courses-nobody-took", "Courses Nobody Took", "joins", "anti-join", "easy",
  """
  Return the `title` of every course that has **no enrollments at all**, in alphabetical order.
  """,
  [COURSES, ENROLLMENTS],
  "SELECT c.title FROM courses c WHERE NOT EXISTS (SELECT 1 FROM enrollments e WHERE e.course_id = c.id) ORDER BY c.title",
  [(ex(SCHOOL_EX, "courses", "enrollments"), "Algebra and Biology have students; Drawing has none.")],
  lambda rng, n, k: empty_courses(rng, n, k),
  ordered=True,
  wrong=["SELECT c.title FROM courses c JOIN enrollments e ON e.course_id = c.id GROUP BY c.id HAVING COUNT(*) = 0 ORDER BY c.title",
         "SELECT c.title FROM courses c LEFT JOIN enrollments e ON e.course_id = c.id WHERE e.score IS NULL ORDER BY c.title"])

P("order-totals", "Order Totals", "joins", "multi-join", "medium",
  """
  Each order has items, and each item is a product bought in some `quantity`. An order's total is the sum of
  `quantity × price` over its items.

  For every **delivered** order, return `order_id`, the customer's `name` and the order's `total`, rounded to 2 decimal
  places. Any order.
  """,
  [CUSTOMERS, PRODUCTS, ORDERS, ORDER_ITEMS],
  """
  SELECT o.id AS order_id, c.name, ROUND(SUM(i.quantity * p.price), 2) AS total
  FROM orders o
  JOIN customers c ON c.id = o.customer_id
  JOIN order_items i ON i.order_id = o.id
  JOIN products p ON p.id = i.product_id
  WHERE o.status = 'delivered'
  GROUP BY o.id, c.name
  """,
  [(SHOP_EX, "Order 1 is two Kettles (49.00) and a Novel (12.00): 61.00. Order 3 is two Comics: 13.00.")],
  lambda rng, n, k: shop(rng, n, k),
  wrong=["SELECT o.id AS order_id, c.name, ROUND(SUM(p.price), 2) AS total FROM orders o JOIN customers c ON c.id = o.customer_id JOIN order_items i ON i.order_id = o.id JOIN products p ON p.id = i.product_id WHERE o.status = 'delivered' GROUP BY o.id, c.name",
         "SELECT o.id AS order_id, c.name, ROUND(SUM(i.quantity * p.price), 2) AS total FROM orders o JOIN customers c ON c.id = o.customer_id JOIN order_items i ON i.order_id = o.id JOIN products p ON p.id = i.order_id WHERE o.status = 'delivered' GROUP BY o.id, c.name"])

P("lifetime-spend", "Lifetime Spend", "joins", "multi-join", "hard",
  """
  Rank every customer by how much they've spent on **delivered** orders. Customers who haven't spent anything yet still
  appear, with `0`.

  Return `name` and `spent` (the sum of `quantity × price` over their delivered orders' items, rounded to 2 decimal
  places). Order by `spent` from most to least, then by `name`.
  """,
  [CUSTOMERS, PRODUCTS, ORDERS, ORDER_ITEMS],
  """
  SELECT c.name, ROUND(COALESCE(SUM(i.quantity * p.price), 0), 2) AS spent
  FROM customers c
  LEFT JOIN orders o ON o.customer_id = c.id AND o.status = 'delivered'
  LEFT JOIN order_items i ON i.order_id = o.id
  LEFT JOIN products p ON p.id = i.product_id
  GROUP BY c.id, c.name
  ORDER BY spent DESC, c.name
  """,
  [(SHOP_EX, "Omar's delivered orders come to 61.00 + 13.00 = 74.00. Elif's order hasn't arrived and Priya's was cancelled, so they and Uma show 0.")],
  lambda rng, n, k: shop(rng, n, k),
  ordered=True,
  wrong=["SELECT c.name, ROUND(COALESCE(SUM(i.quantity * p.price), 0), 2) AS spent FROM customers c LEFT JOIN orders o ON o.customer_id = c.id LEFT JOIN order_items i ON i.order_id = o.id LEFT JOIN products p ON p.id = i.product_id WHERE o.status = 'delivered' GROUP BY c.id, c.name ORDER BY spent DESC, c.name",
         "SELECT c.name, ROUND(COALESCE(SUM(i.quantity * p.price), 0), 2) AS spent FROM customers c LEFT JOIN orders o ON o.customer_id = c.id LEFT JOIN order_items i ON i.order_id = o.id LEFT JOIN products p ON p.id = i.product_id GROUP BY c.id, c.name ORDER BY spent DESC, c.name"],
  notes="A condition on the right-hand table of a LEFT JOIN belongs in the `ON` clause. In `WHERE`, it throws away the unmatched rows and the join behaves like an inner join.")

P("out-earning-the-boss", "Out-earning the Boss", "joins", "self-join", "easy",
  """
  `manager_id` points to another row of `employees`. Find everyone who earns **more than their manager**.

  Return the employee's `name`, their `salary`, and their manager's name as `manager`, in any order.
  """,
  [EMPLOYEES],
  "SELECT e.name, e.salary, m.name AS manager FROM employees e JOIN employees m ON m.id = e.manager_id WHERE e.salary > m.salary",
  [(ex(STAFF_EX, "employees"), "Dara earns 125,500 and her manager Bilal earns 61,000. Everyone else earns less than their manager, and Ava has no manager.")],
  lambda rng, n, k: only(staff(rng, n, k), "employees"),
  wrong=["SELECT e.name, e.salary, m.name AS manager FROM employees e JOIN employees m ON m.manager_id = e.id WHERE e.salary > m.salary",
         "SELECT e.name, e.salary, m.name AS manager FROM employees e JOIN employees m ON m.id = e.manager_id WHERE e.salary >= m.salary"])

P("same-city-pairs", "Neighbours in the Same City", "joins", "self-join", "medium",
  """
  The shop wants to suggest shared deliveries. List every **pair** of customers who live in the same city.

  Return `first` and `second`: the two customers' names, with the smaller `id` as `first`. Each pair appears once.
  Any order.
  """,
  [CUSTOMERS],
  "SELECT a.name AS first, b.name AS second FROM customers a JOIN customers b ON a.city = b.city AND a.id < b.id",
  [(ex(SHOP_EX, "customers"), "Omar (id 1) and Uma (id 4) both live in Osaka. Nobody else shares a city.")],
  lambda rng, n, k: only(shop(rng, n, k), "customers"),
  wrong=["SELECT a.name AS first, b.name AS second FROM customers a JOIN customers b ON a.city = b.city AND a.id <> b.id",
         "SELECT a.name AS first, b.name AS second FROM customers a JOIN customers b ON a.city = b.city AND a.id <= b.id"],
  sizes=[2, 3, 4, 6, 8, 12, 16, 24, 40, 60, 90, 140])

P("attendance-sheet", "Attendance Sheet", "joins", "cross-join", "medium",
  """
  The office prints a grid with **every student next to every course**, marking whether the student is enrolled.

  Return the student's `name`, the course `title`, and `enrolled`: `1` if the student is enrolled in that course,
  otherwise `0`. Order by `name`, then `title`.
  """,
  [STUDENTS, COURSES, ENROLLMENTS],
  """
  SELECT s.name, c.title,
         CASE WHEN e.student_id IS NULL THEN 0 ELSE 1 END AS enrolled
  FROM students s
  CROSS JOIN courses c
  LEFT JOIN enrollments e ON e.student_id = s.id AND e.course_id = c.id
  ORDER BY s.name, c.title
  """,
  [(SCHOOL_EX, "3 students × 3 courses = 9 rows. Ava takes Algebra and Biology (her Biology score isn't in yet, but she's still enrolled); Bilal takes Algebra.")],
  lambda rng, n, k: school(rng, n, k),
  ordered=True,
  wrong=["SELECT s.name, c.title, CASE WHEN e.score IS NULL THEN 0 ELSE 1 END AS enrolled FROM students s CROSS JOIN courses c LEFT JOIN enrollments e ON e.student_id = s.id AND e.course_id = c.id ORDER BY s.name, c.title",
         "SELECT s.name, c.title, 1 AS enrolled FROM students s JOIN enrollments e ON e.student_id = s.id JOIN courses c ON c.id = e.course_id ORDER BY s.name, c.title"],
  sizes=[1, 2, 3, 4, 6, 9, 14, 20, 30, 50, 90, 150])

# --- Set operations ------------------------------------------------------------------------------

SUPPLIERS = T("suppliers", ("id", "INTEGER", "pk"), ("name", "TEXT"), ("city", "TEXT"))
TOWNS = ["Lisbon", "Osaka", "Nairobi", "Denver", "Pune", "Quito"]


def touch_gen(rng, n, k):
    customers = [(i + 1, nm, rng.choice(TOWNS[:4]), "2023-01-01") for i, nm in enumerate(names(rng, n))]
    suppliers = [(i + 1, f"{rng.choice(['North', 'Blue', 'Oak', 'Iron'])} {rng.choice(['Mills', 'Works', 'Goods'])} {i + 1}", rng.choice(TOWNS[2:])) for i in range(max(1, n // 2))]
    return {"customers": customers, "suppliers": suppliers}

P("cities-we-touch", "Cities We Touch", "set-ops", "union", "easy",
  """
  A city matters to the business if a customer lives there **or** a supplier is based there.

  Return each such city once, as `city`, in alphabetical order.
  """,
  [CUSTOMERS, SUPPLIERS],
  "SELECT city FROM customers UNION SELECT city FROM suppliers ORDER BY city",
  [({"customers": SHOP_EX["customers"], "suppliers": [(1, "Oak Mills", "Pune"), (2, "Blue Works", "Osaka")]},
    "Customers live in Osaka, Lisbon and Denver; suppliers are in Pune and Osaka. Osaka is listed once.")],
  touch_gen,
  ordered=True,
  wrong=["SELECT city FROM customers UNION ALL SELECT city FROM suppliers ORDER BY city",
         "SELECT DISTINCT city FROM customers ORDER BY city"])

DEPOSITS = T("deposits", ("account_id", "INTEGER"), ("amount", "INTEGER"), ("made_on", "TEXT"))
WITHDRAWALS = T("withdrawals", ("account_id", "INTEGER"), ("amount", "INTEGER"), ("made_on", "TEXT"))


def ledger_gen(rng, n, k):
    accounts = max(1, n // 3 + 1)
    dep, wd = [], []
    for _ in range(n):
        amt = rng.choice([50, 100]) if ties(k) else rng.randint(1, 500)
        d = day(rng.randint(0, 2 if ties(k) else 60))
        (dep if rng.random() < 0.6 else wd).append((rng.randint(1, accounts), amt, d))
    if not dep:
        dep.append((1, 10, day(0)))
    return {"deposits": dep, "withdrawals": wd}

P("account-balances", "Account Balances", "set-ops", "union", "medium",
  """
  Money moves in through `deposits` and out through `withdrawals`. An account's balance is everything deposited minus
  everything withdrawn.

  Return `account_id` and `balance` for every account that appears in either table, in any order.
  """,
  [DEPOSITS, WITHDRAWALS],
  """
  SELECT account_id, SUM(amount) AS balance
  FROM (SELECT account_id, amount FROM deposits
        UNION ALL
        SELECT account_id, -amount FROM withdrawals)
  GROUP BY account_id
  """,
  [({"deposits": [(1, 100, "2024-01-02"), (1, 100, "2024-01-02"), (2, 40, "2024-01-05")],
     "withdrawals": [(1, 30, "2024-01-09"), (3, 20, "2024-01-10")]},
    "Account 1 made the same 100 deposit twice, so it has 200 − 30 = 170. Account 3 only withdrew: −20.")],
  ledger_gen,
  wrong=["SELECT account_id, SUM(amount) AS balance FROM (SELECT account_id, amount FROM deposits UNION SELECT account_id, -amount FROM withdrawals) GROUP BY account_id",
         "SELECT d.account_id, SUM(d.amount) - COALESCE(SUM(w.amount), 0) AS balance FROM deposits d LEFT JOIN withdrawals w ON w.account_id = d.account_id GROUP BY d.account_id"],
  notes="`UNION` removes duplicate rows, so two identical deposits would count once. `UNION ALL` keeps every row.")

BOOK_CLUB = T("book_club", ("name", "TEXT"))
FILM_CLUB = T("film_club", ("name", "TEXT"))


def clubs_gen(rng, n, k):
    pool = FIRST[: max(4, n + 3)]
    book = [(rng.choice(pool),) for _ in range(n)]
    film = [(rng.choice(pool),) for _ in range(max(1, n - 1))]
    film.append((book[0][0],))  # at least one person in both
    return {"book_club": book, "film_club": film}

P("both-clubs", "Members of Both Clubs", "set-ops", "intersect-except", "easy",
  """
  The book club and the film club each keep a sign-up sheet. Some people signed a sheet more than once.

  Return the `name` of everyone on **both** sheets, each name once, in alphabetical order.
  """,
  [BOOK_CLUB, FILM_CLUB],
  "SELECT name FROM book_club INTERSECT SELECT name FROM film_club ORDER BY name",
  [({"book_club": [("Nia",), ("Omar",), ("Nia",), ("Rosa",)], "film_club": [("Rosa",), ("Nia",), ("Tara",)]},
    "Nia and Rosa are on both sheets. Nia signed the book club twice but is listed once.")],
  clubs_gen,
  ordered=True,
  wrong=["SELECT b.name FROM book_club b JOIN film_club f ON f.name = b.name ORDER BY b.name",
         "SELECT name FROM book_club UNION SELECT name FROM film_club ORDER BY name"])

SUBSCRIBERS = T("subscribers", ("email", "TEXT"))
BUYERS = T("buyers", ("email", "TEXT"))


def winback_gen(rng, n, k):
    pool = [f"{f.lower()}@mail.test" for f in FIRST[: max(4, n + 3)]]
    subs = [(rng.choice(pool),) for _ in range(n + 1)]
    buys = [(rng.choice(pool),) for _ in range(max(1, n // 2))]
    return {"subscribers": subs, "buyers": buys}

P("win-back-list", "Win-back List", "set-ops", "intersect-except", "easy",
  """
  Marketing wants to email newsletter subscribers who have **never bought anything**. Both lists can repeat an email.

  Return each such `email` once, in alphabetical order.
  """,
  [SUBSCRIBERS, BUYERS],
  "SELECT email FROM subscribers EXCEPT SELECT email FROM buyers ORDER BY email",
  [({"subscribers": [("gus@mail.test",), ("ava@mail.test",), ("gus@mail.test",), ("ivo@mail.test",)], "buyers": [("ava@mail.test",)]},
    "Ava bought something. Gus subscribed twice and appears once.")],
  winback_gen,
  ordered=True,
  wrong=["SELECT email FROM subscribers WHERE email NOT IN (SELECT email FROM buyers) ORDER BY email",
         "SELECT email FROM buyers EXCEPT SELECT email FROM subscribers ORDER BY email"])

# --- Subqueries ---------------------------------------------------------------------------------

P("above-average-earners", "Above-average Earners", "subqueries", "scalar-subquery", "easy",
  """
  Return the `name` and `salary` of every employee who earns **more than the company's average salary** (every
  employee counts toward the average). Order by `salary` from high to low, then by `name`.
  """,
  [EMPLOYEES],
  "SELECT name, salary FROM employees WHERE salary > (SELECT AVG(salary) FROM employees) ORDER BY salary DESC, name",
  [(ex(STAFF_EX, "employees"), "The average is 78,100. Dara (125,500) and Ava (96,000) earn more.")],
  lambda rng, n, k: only(staff(rng, n, k), "employees"),
  ordered=True,
  wrong=["SELECT name, salary FROM employees WHERE salary > (SELECT AVG(salary) FROM employees WHERE dept_id IS NOT NULL) ORDER BY salary DESC, name",
         "SELECT name, salary FROM employees WHERE salary >= (SELECT AVG(salary) FROM employees) ORDER BY salary DESC, name"])

P("book-buyers", "Book Buyers", "subqueries", "in-exists", "medium",
  """
  Find the customers who have bought **at least one product in the Books category**, in any order and whatever the
  order's status.

  Return each such customer's `name` once. Any order.
  """,
  [CUSTOMERS, PRODUCTS, ORDERS, ORDER_ITEMS],
  """
  SELECT c.name FROM customers c
  WHERE EXISTS (
    SELECT 1 FROM orders o
    JOIN order_items i ON i.order_id = o.id
    JOIN products p ON p.id = i.product_id
    WHERE o.customer_id = c.id AND p.category = 'Books'
  )
  """,
  [(SHOP_EX, "Omar bought a Novel and Comics; Elif's order has a Novel. Priya only ordered Kites, and Uma ordered nothing.")],
  lambda rng, n, k: shop(rng, n, k),
  wrong=["SELECT c.name FROM customers c JOIN orders o ON o.customer_id = c.id JOIN order_items i ON i.order_id = o.id JOIN products p ON p.id = i.product_id WHERE p.category = 'Books'",
         "SELECT c.name FROM customers c WHERE c.id IN (SELECT o.customer_id FROM orders o JOIN order_items i ON i.order_id = o.id JOIN products p ON p.id = i.product_id WHERE p.category = 'Books' AND o.status = 'delivered')"])

P("above-department-average", "Above the Department Average", "subqueries", "correlated", "medium",
  """
  Find the employees who earn **more than the average salary of their own department**.

  Return the `department` name, the employee's `name` and `salary`, in any order. Employees without a department are
  left out.
  """,
  [DEPARTMENTS, EMPLOYEES],
  """
  SELECT d.name AS department, e.name, e.salary
  FROM employees e
  JOIN departments d ON d.id = e.dept_id
  WHERE e.salary > (SELECT AVG(x.salary) FROM employees x WHERE x.dept_id = e.dept_id)
  """,
  [(STAFF_EX, "Design averages 78,000, so Ava (96,000) is returned and Chen (60,000) isn't. Sales averages 54,500: Bilal is returned.")],
  lambda rng, n, k: staff(rng, n, k),
  wrong=["SELECT d.name AS department, e.name, e.salary FROM employees e JOIN departments d ON d.id = e.dept_id WHERE e.salary > (SELECT AVG(salary) FROM employees)",
         "SELECT d.name AS department, e.name, e.salary FROM employees e JOIN departments d ON d.id = e.dept_id WHERE e.salary >= (SELECT AVG(x.salary) FROM employees x WHERE x.dept_id = e.dept_id)"])

# --- CTEs ---------------------------------------------------------------------------------------------

P("departments-above-company", "Departments That Pay Above Average", "ctes", "step-ctes", "medium",
  """
  Compare each department's average salary with the **company-wide** average (every employee counts toward the
  company average, including those without a department).

  Return the department's `name` and its `avg_salary`, rounded to 2 decimal places, for every department whose average
  is higher than the company's. Any order.
  """,
  [DEPARTMENTS, EMPLOYEES],
  """
  WITH dept AS (
    SELECT dept_id, AVG(salary) AS avg_salary
    FROM employees
    WHERE dept_id IS NOT NULL
    GROUP BY dept_id
  ),
  company AS (
    SELECT AVG(salary) AS avg_salary FROM employees
  )
  SELECT d.name, ROUND(dept.avg_salary, 2) AS avg_salary
  FROM dept
  JOIN departments d ON d.id = dept.dept_id
  CROSS JOIN company
  WHERE dept.avg_salary > company.avg_salary
  """,
  [({"departments": STAFF_EX["departments"], "employees": STAFF_EX["employees"] + [(6, "Fern Lund", 3, 4, 110000, "2023-02-01")]},
    "The company average is 500,500 / 6 = 83,416.67. Legal (110,000) is above it; Design (78,000) and Sales (54,500) aren't.")],
  lambda rng, n, k: staff(rng, n, k, empty_depts=False),
  wrong=["WITH dept AS (SELECT dept_id, AVG(salary) AS avg_salary FROM employees GROUP BY dept_id), company AS (SELECT AVG(salary) AS avg_salary FROM employees WHERE dept_id IS NOT NULL) SELECT d.name, ROUND(dept.avg_salary, 2) AS avg_salary FROM dept JOIN departments d ON d.id = dept.dept_id CROSS JOIN company WHERE dept.avg_salary > company.avg_salary",
         "SELECT d.name, ROUND(AVG(e.salary), 2) AS avg_salary FROM employees e JOIN departments d ON d.id = e.dept_id GROUP BY d.id, d.name HAVING AVG(e.salary) > 80000"])

# --- Strings & dates ----------------------------------------------------------------------------------

ACCOUNTS = T("accounts", ("id", "INTEGER", "pk"), ("email", "TEXT"))
DOMAINS = ["mail.test", "inbox.example", "post.dev", "ren.example"]


def accounts_gen(rng, n, k):
    rows = []
    for i in range(n):
        user = rng.choice(FIRST).lower() + (str(rng.randint(1, 99)) if rng.random() < 0.4 else "") + (rng.choice(["", ".x", "_dev"]) if not ties(k) else "")
        rows.append((i + 1, f"{user}@{rng.choice(DOMAINS)}"))
    return {"accounts": rows}

P("split-emails", "Split the Emails", "strings-dates", "string-functions", "easy",
  """
  Every email has a username before the `@` and a domain after it.

  Return each account's `id`, its `username` and its `domain`, in any order.
  """,
  [ACCOUNTS],
  """
  SELECT id,
         substr(email, 1, instr(email, '@') - 1) AS username,
         substr(email, instr(email, '@') + 1) AS domain
  FROM accounts
  """,
  [({"accounts": [(1, "kofi@mail.test"), (2, "lena.x@post.dev"), (3, "mateo42@inbox.example")]},
    "For `lena.x@post.dev` the `@` is the 7th character, so the username is the first 6 characters and the domain is everything after.")],
  accounts_gen,
  wrong=["SELECT id, substr(email, 1, instr(email, '@')) AS username, substr(email, instr(email, '@') + 1) AS domain FROM accounts",
         "SELECT id, substr(email, 1, instr(email, '@') - 1) AS username, substr(email, instr(email, '@')) AS domain FROM accounts"],
  notes="`instr(text, '@')` is the position of the first `@`, counting from 1. `substr(text, start, length)` also counts from 1.")

P("customer-initials", "Initials", "strings-dates", "string-functions", "easy",
  """
  Every customer's `name` is a first name and a last name separated by one space. Name tags show initials like
  `O.F.` for Omar Fox.

  Return each customer's `id` and `initials`, in any order.
  """,
  [CUSTOMERS],
  "SELECT id, substr(name, 1, 1) || '.' || substr(name, instr(name, ' ') + 1, 1) || '.' AS initials FROM customers",
  [(ex(SHOP_EX, "customers"), "Priya Nair becomes `P.N.`: the first letter, a dot, the first letter after the space, a dot.")],
  lambda rng, n, k: only(shop(rng, n * 2, k), "customers"),
  wrong=["SELECT id, substr(name, 1, 1) || substr(name, instr(name, ' ') + 1, 1) AS initials FROM customers",
         "SELECT id, substr(name, 1, 1) || '.' || substr(name, instr(name, ' '), 1) || '.' AS initials FROM customers"])

P("orders-per-month", "Orders per Month", "strings-dates", "date-functions", "easy",
  """
  Count the orders placed in each calendar month.

  Return `month` (written `YYYY-MM`) and `orders`, from the earliest month to the latest. Months with no orders don't
  appear.
  """,
  [ORDERS],
  "SELECT strftime('%Y-%m', ordered_on) AS month, COUNT(*) AS orders FROM orders GROUP BY month ORDER BY month",
  [(ex(SHOP_EX, "orders"), "Two orders in January 2024 and two in February.")],
  lambda rng, n, k: only(shop(rng, n, k, start=(2023, 10, 1), span=420), "orders"),
  ordered=True,
  wrong=["SELECT strftime('%m', ordered_on) AS month, COUNT(*) AS orders FROM orders GROUP BY month ORDER BY month",
         "SELECT strftime('%Y-%m', ordered_on) AS month, COUNT(DISTINCT customer_id) AS orders FROM orders GROUP BY month ORDER BY month"],
  notes="`strftime('%Y-%m', '2024-02-11')` gives `'2024-02'`.")

SHIPMENTS = T("shipments", ("order_id", "INTEGER", "pk"), ("ordered_on", "TEXT"), ("shipped_on", "TEXT"))


def ship_gen(rng, n, k):
    rows = []
    for i in range(n + 1):
        start = rng.randint(0, 120)
        gap = rng.choice([2, 3, 4]) if ties(k) else rng.randint(0, 9)
        rows.append((i + 1, day(start), maybe(rng, 0.2, day(start + gap))))
    return {"shipments": rows}

P("slow-shipments", "Slow Shipments", "strings-dates", "date-functions", "medium",
  """
  An order ships slowly if it took **more than 3 days** from `ordered_on` to `shipped_on`. Orders that haven't shipped
  yet (`shipped_on` is NULL) don't count.

  Return `order_id` and `days` (the whole number of days it took), slowest first; break ties by `order_id`.
  """,
  [SHIPMENTS],
  """
  SELECT order_id, CAST(julianday(shipped_on) - julianday(ordered_on) AS INTEGER) AS days
  FROM shipments
  WHERE julianday(shipped_on) - julianday(ordered_on) > 3
  ORDER BY days DESC, order_id
  """,
  [({"shipments": [(1, "2024-01-30", "2024-02-02"), (2, "2024-01-28", "2024-02-03"), (3, "2024-02-01", None), (4, "2024-02-05", "2024-02-09")]},
    "Order 2 took 6 days (across the end of January) and order 4 took 4. Order 1 took exactly 3, which isn't more than 3.")],
  ship_gen,
  ordered=True,
  wrong=["SELECT order_id, CAST(strftime('%d', shipped_on) - strftime('%d', ordered_on) AS INTEGER) AS days FROM shipments WHERE strftime('%d', shipped_on) - strftime('%d', ordered_on) > 3 ORDER BY days DESC, order_id",
         "SELECT order_id, CAST(julianday(shipped_on) - julianday(ordered_on) AS INTEGER) AS days FROM shipments WHERE julianday(shipped_on) - julianday(ordered_on) >= 3 ORDER BY days DESC, order_id"],
  notes="`julianday()` turns a date into a day number, so subtracting two of them gives the days between.")

done()
