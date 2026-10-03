"""Shared little worlds the problems are set in, with random-data builders.

Each builder takes (rng, n, k): n is the scale, k the hidden test's number.
k % 3 == 0 makes values collide (ties), k % 3 == 1 sprinkles NULLs where a
column allows them, k % 3 == 2 is plain random data.
"""
from author import CITIES, T, day, firsts, maybe, names

ties = lambda k: k % 3 == 0  # noqa: E731
nully = lambda k: k % 3 == 1  # noqa: E731

# --- A company: departments and employees ------------------------------------

DEPARTMENTS = T("departments", ("id", "INTEGER", "pk"), ("name", "TEXT"), ("city", "TEXT"))
EMPLOYEES = T(
    "employees",
    ("id", "INTEGER", "pk"),
    ("name", "TEXT"),
    ("dept_id", "INTEGER", "fk departments.id"),
    ("manager_id", "INTEGER", "fk employees.id"),
    ("salary", "INTEGER"),
    ("hired_on", "TEXT"),
)
DEPT_NAMES = ["Design", "Sales", "Support", "Research", "Finance", "Legal", "Ops", "Data"]


def staff(rng, n, k, empty_depts=True):
    nd = min(len(DEPT_NAMES), max(1, n // 4 + 1))
    depts = [(i + 1, name, rng.choice(CITIES)) for i, name in enumerate(rng.sample(DEPT_NAMES, nd))]
    people = names(rng, n)
    rows = []
    for i in range(n):
        dept = rng.randint(1, nd)
        if empty_depts and nd > 2 and dept == nd:
            dept = rng.randint(1, nd - 1)  # the last department stays empty
        salary = rng.choice([50000, 60000, 70000]) if ties(k) else rng.randrange(40000, 160001, 500)
        manager = rng.randint(1, i) if i and rng.random() < 0.85 else None
        rows.append((i + 1, people[i], maybe(rng, 0.25 if nully(k) else 0, dept), manager, salary, day(rng.randint(0, 1500), (2019, 1, 1))))
    return {"departments": depts, "employees": rows}


# --- A shop: customers, products, orders and order items ---------------------

CUSTOMERS = T("customers", ("id", "INTEGER", "pk"), ("name", "TEXT"), ("city", "TEXT"), ("joined_on", "TEXT"))
PRODUCTS = T("products", ("id", "INTEGER", "pk"), ("name", "TEXT"), ("category", "TEXT"), ("price", "REAL"))
ORDERS = T("orders", ("id", "INTEGER", "pk"), ("customer_id", "INTEGER", "fk customers.id"), ("ordered_on", "TEXT"), ("status", "TEXT"))
ORDER_ITEMS = T("order_items", ("order_id", "INTEGER", "fk orders.id"), ("product_id", "INTEGER", "fk products.id"), ("quantity", "INTEGER"))

CATEGORIES = ["Books", "Games", "Garden", "Kitchen", "Music", "Toys"]
GOODS = """Atlas Lamp Kettle Puzzle Trowel Novel Vinyl Blender Kite Chess Planter Teapot Drum Comic Skillet Seeds
Ukulele Domino Whisk Poster Hammock Journal Mixer Yo-yo Rake Cookbook Banjo Marble Grater Frisbee""".split()
STATUSES = ["delivered", "shipped", "cancelled"]


def shop(rng, n, k, start=(2024, 1, 1), span=180):
    nc = max(1, n // 2 + 1)
    np_ = min(len(GOODS), max(2, n // 3 + 2))
    customers = [(i + 1, nm, rng.choice(CITIES[:4]), day(rng.randint(0, 300), (2023, 1, 1))) for i, nm in enumerate(names(rng, nc))]
    products = []
    for i, g in enumerate(rng.sample(GOODS, np_)):
        price = rng.choice([10.0, 20.0, 30.0]) if ties(k) else round(rng.uniform(3, 120), 2)
        products.append((i + 1, g, rng.choice(CATEGORIES[: max(2, min(6, np_ // 2))]), price))
    orders, items = [], []
    for i in range(n):
        orders.append((i + 1, rng.randint(1, nc), day(rng.randint(0, span), start), rng.choice(STATUSES) if rng.random() < 0.4 else "delivered"))
        for pid in rng.sample(range(1, np_ + 1), rng.randint(1, min(3, np_))):
            items.append((i + 1, pid, rng.randint(1, 2 if ties(k) else 5)))
    return {"customers": customers, "products": products, "orders": orders, "order_items": items}


# --- A school: students, courses and enrollments -----------------------------

STUDENTS = T("students", ("id", "INTEGER", "pk"), ("name", "TEXT"), ("year", "INTEGER"))
COURSES = T("courses", ("id", "INTEGER", "pk"), ("title", "TEXT"), ("credits", "INTEGER"))
ENROLLMENTS = T("enrollments", ("student_id", "INTEGER", "fk students.id"), ("course_id", "INTEGER", "fk courses.id"), ("score", "INTEGER"))
COURSE_TITLES = ["Algebra", "Biology", "Chemistry", "Drawing", "Economics", "French", "Geography", "History", "Poetry", "Physics"]


def school(rng, n, k):
    nc = min(len(COURSE_TITLES), max(2, n // 3 + 2))
    students = [(i + 1, nm, rng.randint(1, 4)) for i, nm in enumerate(firsts(rng, n))]
    courses = [(i + 1, t, rng.choice([2, 3, 4])) for i, t in enumerate(rng.sample(COURSE_TITLES, nc))]
    enroll = []
    for s in range(1, n + 1):
        if rng.random() < 0.15:
            continue  # some students take nothing
        for c in rng.sample(range(1, nc + 1), rng.randint(1, min(4, nc))):
            score = rng.choice([70, 80, 90]) if ties(k) else rng.randint(35, 100)
            enroll.append((s, c, maybe(rng, 0.2 if nully(k) else 0, score)))
    return {"students": students, "courses": courses, "enrollments": enroll}


# --- An app: users and their daily logins ------------------------------------

USERS = T("users", ("id", "INTEGER", "pk"), ("name", "TEXT"), ("country", "TEXT"), ("signed_up", "TEXT"))
LOGINS = T("logins", ("user_id", "INTEGER", "fk users.id"), ("login_on", "TEXT"))
COUNTRIES = ["BR", "CA", "DE", "IN", "JP", "KE", "MX", "NZ"]


def app(rng, n, k, days=40, repeat=True):
    nu = max(1, n // 3 + 1)
    users = []
    logins = []
    for i, nm in enumerate(names(rng, nu)):
        start = rng.randint(0, days // 2)
        users.append((i + 1, nm, rng.choice(COUNTRIES[:4]), day(start)))
        d = start
        for _ in range(rng.randint(0, max(1, n // nu * 2))):
            logins.append((i + 1, day(d)))
            if repeat and rng.random() < 0.15:
                logins.append((i + 1, day(d)))  # the same day twice
            d += rng.choice([1, 1, 1, 2, 3, 6])
    rng.shuffle(logins)
    return {"users": users, "logins": logins}
