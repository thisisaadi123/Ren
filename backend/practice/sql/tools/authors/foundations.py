"""Foundations: selecting & filtering, sorting & limiting, aggregation, conditional logic."""
import _common  # noqa: F401
from _common import only
from author import CITIES, P, T, day, done, maybe, names
from worlds import CUSTOMERS, EMPLOYEES, ORDERS, PRODUCTS, nully, shop, staff, ties

EMP_EX = {"employees": [
    (1, "Ava Moss", 1, None, 96000, "2019-03-04"),
    (2, "Bilal Cruz", 2, 1, 61000, "2020-07-15"),
    (3, "Chen Ito", 1, 1, 60000, "2021-01-10"),
    (4, "Dara Kerr", None, 2, 125500, "2019-03-04"),
    (5, "Elif Park", 2, 2, 48000, "2022-11-30"),
]}

# --- Selecting & filtering ---------------------------------------------------------------

P("monthly-pay", "Monthly Pay", "select-filter", "pick-columns", "easy",
  """
  The `employees` table stores each person's yearly `salary`. Payroll wants to see what everyone earns per month.

  Return each employee's `name` and their `monthly` pay: the salary divided by 12, rounded to 2 decimal places.

  Return the rows in any order.
  """,
  [EMPLOYEES],
  "SELECT name, ROUND(salary / 12.0, 2) AS monthly FROM employees",
  [(EMP_EX, """
    Ava earns 96,000 a year, which is exactly 8,000 a month. Bilal's 61,000 / 12 = 5,083.333…, so 5083.33.
    """)],
  lambda rng, n, k: only(staff(rng, n, k), "employees"),
  wrong=["SELECT name, salary / 12 AS monthly FROM employees",
         "SELECT name, ROUND(salary / 12.0) AS monthly FROM employees"],
  notes="""
  In SQLite, dividing two whole numbers gives a whole number: `61000 / 12` is `5083`. Divide by `12.0` to keep the fraction.
  """)

PROD_EX = {"products": [
    (1, "Kettle", "Kitchen", 24.5), (2, "Trowel", "Garden", 10.0), (3, "Blender", "Kitchen", 89.99),
    (4, "Novel", "Books", 12.0), (5, "Planter", "Garden", 50.0), (6, "Whisk", "Kitchen", 6.75),
]}

P("home-and-garden-picks", "Home and Garden Picks", "select-filter", "where-conditions", "easy",
  """
  A gift guide only features products from the **Kitchen** or **Garden** categories that cost **between 10 and 50**,
  both ends included.

  Return the `name` and `price` of every product that qualifies, in any order.
  """,
  [PRODUCTS],
  "SELECT name, price FROM products WHERE category IN ('Kitchen', 'Garden') AND price BETWEEN 10 AND 50",
  [(PROD_EX, """
    The Kettle (24.50), Trowel (exactly 10) and Planter (exactly 50) qualify. The Blender costs too much, the Whisk too
    little, and the Novel is in Books.
    """)],
  lambda rng, n, k: only(shop(rng, n * 2, k), "products"),
  wrong=["SELECT name, price FROM products WHERE category = 'Kitchen' OR category = 'Garden' AND price BETWEEN 10 AND 50",
         "SELECT name, price FROM products WHERE category IN ('Kitchen', 'Garden') AND price > 10 AND price < 50"],
  sizes=[2, 4, 6, 10, 14, 20, 30, 40, 60, 90])


def vowel_gen(rng, n, k):
    d = only(shop(rng, n * 2, k), "customers")
    return d

CUST_EX = {"customers": [
    (1, "Omar Fox", "Osaka", "2023-02-01"), (2, "Priya Nair", "Lisbon", "2023-05-12"),
    (3, "Elif Gray", "Denver", "2023-01-20"), (4, "Uma Sato", "Osaka", "2023-08-03"), (5, "Gus Holt", "Nairobi", "2023-03-15"),
]}

P("vowel-names", "Names That Start with a Vowel", "select-filter", "where-conditions", "easy",
  """
  Marketing is testing a greeting that only works for names starting with a vowel.

  Return the `name` of every customer whose name starts with **A, E, I, O or U**, in any order.
  """,
  [CUSTOMERS],
  "SELECT name FROM customers WHERE substr(name, 1, 1) IN ('A', 'E', 'I', 'O', 'U')",
  [(CUST_EX, "Omar, Elif and Uma start with a vowel; Priya and Gus don't.")],
  vowel_gen,
  wrong=["SELECT name FROM customers WHERE name LIKE 'A%' OR name LIKE 'E%' OR name LIKE 'I%'",
         "SELECT name FROM customers WHERE substr(name, 2, 1) IN ('a', 'e', 'i', 'o', 'u')"],
  sizes=[3, 4, 6, 8, 10, 15, 20, 30, 45, 70])


def unassigned_gen(rng, n, k):
    d = only(staff(rng, n + 1, k), "employees")
    rows = [list(r) for r in d["employees"]]
    for r in rng.sample(rows, max(1, len(rows) // 4)):
        r[2] = None
    return {"employees": rows}

P("unassigned-staff", "Unassigned Staff", "select-filter", "null-checks", "easy",
  """
  Some employees haven't been placed in a department yet: their `dept_id` is NULL.

  Return the `id` and `name` of every employee without a department, in any order.
  """,
  [EMPLOYEES],
  "SELECT id, name FROM employees WHERE dept_id IS NULL",
  [(EMP_EX, "Only Dara Kerr has no department.")],
  unassigned_gen,
  wrong=["SELECT id, name FROM employees WHERE dept_id = NULL",
         "SELECT id, name FROM employees WHERE dept_id IS NOT NULL"],
  notes="`NULL = NULL` is not true in SQL, it's unknown, so `dept_id = NULL` never matches. Use `IS NULL`.")

CONTACTS = T("contacts", ("id", "INTEGER", "pk"), ("name", "TEXT"), ("phone", "TEXT"), ("email", "TEXT"))


def contacts_gen(rng, n, k):
    rows = []
    for i, nm in enumerate(names(rng, n)):
        phone = maybe(rng, 0.5, f"555-{rng.randint(1000, 9999)}")
        email = maybe(rng, 0.5, nm.split()[0].lower() + "@mail.test")
        rows.append((i + 1, nm, phone, email))
    return {"contacts": rows}

P("best-way-to-reach", "Best Way to Reach", "select-filter", "null-checks", "easy",
  """
  The `contacts` table has a `phone` and an `email` for each person, but either can be missing (NULL).

  Return each contact's `name` and a `reach` column: the phone number if there is one, otherwise the email, and
  `'no contact'` when both are missing. Any order.
  """,
  [CONTACTS],
  "SELECT name, COALESCE(phone, email, 'no contact') AS reach FROM contacts",
  [({"contacts": [(1, "Hana Lund", "555-0142", "hana@mail.test"), (2, "Ivo Diaz", None, "ivo@mail.test"), (3, "Jae Reyes", None, None)]},
    "Hana has a phone, so it wins. Ivo only has an email. Jae has neither.")],
  contacts_gen,
  wrong=["SELECT name, COALESCE(email, phone, 'no contact') AS reach FROM contacts",
         "SELECT name, COALESCE(phone, email) AS reach FROM contacts"])

# --- Sorting & limiting ----------------------------------------------------------------------

P("seniority-list", "Seniority List", "sort-limit", "order-by", "easy",
  """
  For the anniversary party, list employees from the longest-serving to the newest.

  Return `name` and `hired_on`, ordered by `hired_on` from earliest to latest. People hired on the same day are listed
  by `name`, A to Z.
  """,
  [EMPLOYEES],
  "SELECT name, hired_on FROM employees ORDER BY hired_on, name",
  [(EMP_EX, "Ava and Dara were both hired on 2019-03-04; Ava comes first by name.")],
  lambda rng, n, k: only(staff(rng, n, k), "employees"),
  ordered=True,
  wrong=["SELECT name, hired_on FROM employees ORDER BY hired_on DESC, name",
         "SELECT name, hired_on FROM employees ORDER BY name"],
  notes="Dates are stored as text like `2019-03-04`, which sorts the same way as the dates themselves.")

P("three-priciest", "The Three Priciest", "sort-limit", "top-n", "easy",
  """
  Show the three most expensive products for the shop's front window.

  Return `name` and `price` of the **3** priciest products, most expensive first. Equal prices are ordered by `name`,
  A to Z. If there are fewer than 3 products, return them all.
  """,
  [PRODUCTS],
  "SELECT name, price FROM products ORDER BY price DESC, name LIMIT 3",
  [(PROD_EX, "The Blender (89.99), Planter (50) and Kettle (24.50) cost the most.")],
  lambda rng, n, k: only(shop(rng, n * 2, k), "products"),
  ordered=True,
  wrong=["SELECT name, price FROM products ORDER BY price LIMIT 3",
         "SELECT name, price FROM products ORDER BY price DESC LIMIT 3 OFFSET 1"])

P("second-page", "The Second Page", "sort-limit", "top-n", "easy",
  """
  The catalogue lists products alphabetically, **5 per page**.

  Return the `id` and `name` of the products on **page 2**: the 6th to the 10th products when sorted by `name`, A to Z
  (ties by `id`). Page 2 may be short, or empty.
  """,
  [PRODUCTS],
  "SELECT id, name FROM products ORDER BY name, id LIMIT 5 OFFSET 5",
  [({"products": [(i + 1, nm, "Toys", 5.0) for i, nm in enumerate(["Kite", "Atlas", "Drum", "Yo-yo", "Banjo", "Marble", "Chess", "Lamp"])]},
    "Sorted by name: Atlas, Banjo, Chess, Drum, Kite | Lamp, Marble, Yo-yo. Page 2 holds the last three.")],
  lambda rng, n, k: only(shop(rng, n * 3, k), "products"),
  ordered=True,
  wrong=["SELECT id, name FROM products ORDER BY name LIMIT 5 OFFSET 6",
         "SELECT id, name FROM products ORDER BY name, id LIMIT 5"],
  sizes=[3, 4, 5, 6, 8, 10, 14, 20, 30, 50])

P("cities-with-customers", "Cities with Customers", "sort-limit", "distinct-values", "easy",
  """
  Return every city that has at least one customer, each city **once**, in alphabetical order. The column is `city`.
  """,
  [CUSTOMERS],
  "SELECT DISTINCT city FROM customers ORDER BY city",
  [(CUST_EX, "Osaka has two customers but appears once.")],
  lambda rng, n, k: only(shop(rng, n * 2, k), "customers"),
  ordered=True,
  wrong=["SELECT city FROM customers ORDER BY city",
         "SELECT DISTINCT city FROM customers ORDER BY city DESC"])

# --- Aggregation -------------------------------------------------------------------------------

P("payroll-summary", "Payroll Summary", "aggregation", "aggregate-functions", "easy",
  """
  Finance wants one line about the whole payroll.

  Return a single row with:

  - `headcount`: the number of employees
  - `total`: the sum of all salaries
  - `average`: the average salary, rounded to 2 decimal places
  - `lowest` and `highest`: the smallest and largest salary

  Every employee counts, with or without a department.
  """,
  [EMPLOYEES],
  "SELECT COUNT(*) AS headcount, SUM(salary) AS total, ROUND(AVG(salary), 2) AS average, MIN(salary) AS lowest, MAX(salary) AS highest FROM employees",
  [(EMP_EX, "Five people earn 390,500 in total, an average of 78,100.")],
  lambda rng, n, k: only(staff(rng, n, k), "employees"),
  wrong=["SELECT COUNT(dept_id) AS headcount, SUM(salary) AS total, ROUND(AVG(salary), 2) AS average, MIN(salary) AS lowest, MAX(salary) AS highest FROM employees",
         "SELECT COUNT(*) AS headcount, SUM(salary) AS total, AVG(salary) / 1 AS average, MIN(salary) AS lowest, MAX(salary) AS highest FROM employees WHERE dept_id IS NOT NULL"])

P("headcount-by-department", "Headcount by Department", "aggregation", "group-by", "easy",
  """
  For every department that has employees, return:

  - `dept_id`
  - `headcount`: how many employees it has
  - `avg_salary`: their average salary, rounded to 2 decimal places

  Leave out employees with no department. Any order.
  """,
  [EMPLOYEES],
  "SELECT dept_id, COUNT(*) AS headcount, ROUND(AVG(salary), 2) AS avg_salary FROM employees WHERE dept_id IS NOT NULL GROUP BY dept_id",
  [(EMP_EX, "Department 1 has Ava and Chen (average 78,000); department 2 has Bilal and Elif (54,500). Dara has no department.")],
  lambda rng, n, k: only(staff(rng, n, k), "employees"),
  wrong=["SELECT dept_id, COUNT(*) AS headcount, ROUND(AVG(salary), 2) AS avg_salary FROM employees GROUP BY dept_id",
         "SELECT dept_id, COUNT(*) AS headcount, ROUND(SUM(salary) / COUNT(*), 2) AS avg_salary FROM employees WHERE dept_id IS NOT NULL GROUP BY dept_id"])

ORD_EX = {"orders": [
    (1, 1, "2024-01-03", "delivered"), (2, 2, "2024-01-03", "cancelled"), (3, 1, "2024-01-05", "shipped"),
    (4, 3, "2024-01-06", "delivered"), (5, 1, "2024-01-06", "delivered"), (6, 2, "2024-01-09", "delivered"),
    (7, 2, "2024-01-09", "delivered"), (8, 2, "2024-01-10", "shipped"),
]}

P("busiest-days", "Busiest Days", "aggregation", "group-by", "easy",
  """
  Count how many orders were placed on each day.

  Return `ordered_on` and `orders`, busiest day first. Days with the same number of orders go from earliest to latest.
  """,
  [ORDERS],
  "SELECT ordered_on, COUNT(*) AS orders FROM orders GROUP BY ordered_on ORDER BY orders DESC, ordered_on",
  [(ORD_EX, "Three days had two orders each, so they come first in date order; the other two days had one.")],
  lambda rng, n, k: only(shop(rng, n, k, span=max(3, n // 3)), "orders"),
  ordered=True,
  wrong=["SELECT ordered_on, COUNT(*) AS orders FROM orders GROUP BY ordered_on ORDER BY orders DESC",
         "SELECT ordered_on, COUNT(DISTINCT customer_id) AS orders FROM orders GROUP BY ordered_on ORDER BY orders DESC, ordered_on"])

P("regular-customers", "Regular Customers", "aggregation", "having", "easy",
  """
  A customer counts as a **regular** once they've placed **at least 3 orders**, whatever the orders' status.

  Return `customer_id` and `orders` (how many they placed) for every regular, in any order.
  """,
  [ORDERS],
  "SELECT customer_id, COUNT(*) AS orders FROM orders GROUP BY customer_id HAVING COUNT(*) >= 3",
  [(ORD_EX, "Customer 1 placed 3 orders and customer 2 placed 4. Customer 3 placed only one.")],
  lambda rng, n, k: only(shop(rng, n * 2, k), "orders"),
  wrong=["SELECT customer_id, COUNT(*) AS orders FROM orders GROUP BY customer_id HAVING COUNT(*) > 3",
         "SELECT customer_id, COUNT(*) AS orders FROM orders WHERE status = 'delivered' GROUP BY customer_id HAVING COUNT(*) >= 3"])

def lone_star(rng, n, k):
    """Staff plus, every other test, a department of one person who alone earns over 150,000."""
    rows = only(staff(rng, n, k), "employees")["employees"]
    if k % 2 == 0:
        rows.append((len(rows) + 1, "Zane Xu", 9, None, 158000, "2021-06-01"))
    return {"employees": rows}

P("big-departments", "Departments Worth a Party", "aggregation", "having", "medium",
  """
  The company throws a party for every department whose people earn **more than 150,000 in total** and that has
  **at least 2** employees.

  Return `dept_id` and `payroll` (the department's total salary) for those departments, largest payroll first;
  break ties by `dept_id`. Employees with no department don't form a department.
  """,
  [EMPLOYEES],
  "SELECT dept_id, SUM(salary) AS payroll FROM employees WHERE dept_id IS NOT NULL GROUP BY dept_id HAVING SUM(salary) > 150000 AND COUNT(*) >= 2 ORDER BY payroll DESC, dept_id",
  [(EMP_EX, "Department 1 pays 156,000 to two people. Department 2 pays only 109,000. Dara's 125,500 has no department.")],
  lambda rng, n, k: lone_star(rng, n, k),
  ordered=True,
  wrong=["SELECT dept_id, SUM(salary) AS payroll FROM employees GROUP BY dept_id HAVING SUM(salary) > 150000 AND COUNT(*) >= 2 ORDER BY payroll DESC, dept_id",
         "SELECT dept_id, SUM(salary) AS payroll FROM employees WHERE dept_id IS NOT NULL GROUP BY dept_id HAVING SUM(salary) > 150000 ORDER BY payroll DESC, dept_id",
         "SELECT dept_id, SUM(salary) AS payroll FROM employees WHERE dept_id IS NOT NULL AND salary > 150000 GROUP BY dept_id HAVING COUNT(*) >= 2 ORDER BY payroll DESC, dept_id"],
  sizes=[2, 3, 4, 6, 8, 10, 14, 20, 30, 45, 70, 120])

# --- Conditional logic ----------------------------------------------------------------------

P("salary-bands", "Salary Bands", "conditional", "case-when", "easy",
  """
  HR sorts salaries into three bands:

  - `'low'`: under 60,000
  - `'mid'`: from 60,000 up to 99,999
  - `'high'`: 100,000 or more

  Return each employee's `name` and `band`, in any order.
  """,
  [EMPLOYEES],
  """
  SELECT name,
         CASE WHEN salary < 60000 THEN 'low'
              WHEN salary < 100000 THEN 'mid'
              ELSE 'high' END AS band
  FROM employees
  """,
  [(EMP_EX, "Chen earns exactly 60,000, which is the start of 'mid'. Elif's 48,000 is 'low' and Dara's 125,500 is 'high'.")],
  lambda rng, n, k: only(staff(rng, n, k), "employees") if not ties(k) else {"employees": [
      (i + 1, nm, 1, None, rng.choice([59999, 60000, 99999, 100000]), "2020-01-01") for i, nm in enumerate(names(rng, n))]},
  wrong=["SELECT name, CASE WHEN salary <= 60000 THEN 'low' WHEN salary < 100000 THEN 'mid' ELSE 'high' END AS band FROM employees",
         "SELECT name, CASE WHEN salary < 60000 THEN 'low' WHEN salary <= 100000 THEN 'mid' ELSE 'high' END AS band FROM employees"])

P("order-status-board", "Order Status Board", "conditional", "conditional-aggregation", "medium",
  """
  Build one line per customer who has placed orders, with:

  - `customer_id`
  - `total`: all their orders
  - `delivered`: how many were delivered
  - `cancelled`: how many were cancelled

  Any order.
  """,
  [ORDERS],
  """
  SELECT customer_id,
         COUNT(*) AS total,
         SUM(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) AS delivered,
         SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled
  FROM orders
  GROUP BY customer_id
  """,
  [(ORD_EX, "Customer 2 placed 4 orders: 2 delivered, 1 cancelled and 1 still shipping.")],
  lambda rng, n, k: only(shop(rng, n * 2, k), "orders"),
  wrong=["SELECT customer_id, COUNT(*) AS total, COUNT(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) AS delivered, COUNT(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled FROM orders GROUP BY customer_id",
         "SELECT customer_id, COUNT(*) AS total, SUM(status = 'delivered') AS delivered, SUM(status <> 'delivered') AS cancelled FROM orders GROUP BY customer_id"])

done()
