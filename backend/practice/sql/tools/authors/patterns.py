"""Advanced: recursive queries, gaps & islands, reporting patterns."""
import datetime

import _common  # noqa: F401
from _common import only
from author import FIRST, P, T, day, done, firsts, names
from worlds import EMPLOYEES, USERS, app, staff, ties

EMP_EX = {"employees": [
    (1, "Ava Moss", 1, None, 96000, "2019-03-04"),
    (2, "Bilal Cruz", 2, 1, 61000, "2020-07-15"),
    (3, "Chen Ito", 1, 1, 60000, "2021-01-10"),
    (4, "Dara Kerr", None, 2, 125500, "2019-03-04"),
    (5, "Elif Park", 2, 2, 48000, "2022-11-30"),
]}

# --- Recursive queries ------------------------------------------------------------------------

P("org-chart-levels", "Levels of the Org Chart", "recursive", "hierarchies", "hard",
  """
  People with no manager (`manager_id` is NULL) are at **level 1**. Everyone else is one level below their manager.

  Return every employee's `name` and `level`, in any order.
  """,
  [EMPLOYEES],
  """
  WITH RECURSIVE chart(id, level) AS (
    SELECT id, 1 FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, c.level + 1 FROM employees e JOIN chart c ON e.manager_id = c.id
  )
  SELECT e.name, c.level FROM chart c JOIN employees e ON e.id = c.id
  """,
  [(EMP_EX, "Ava has no manager (level 1). Bilal and Chen report to Ava (level 2). Dara and Elif report to Bilal (level 3).")],
  lambda rng, n, k: only(staff(rng, n, k), "employees"),
  wrong=["SELECT name, CASE WHEN manager_id IS NULL THEN 1 ELSE 2 END AS level FROM employees",
         "SELECT e.name, CASE WHEN e.manager_id IS NULL THEN 1 WHEN m.manager_id IS NULL THEN 2 ELSE 3 END AS level FROM employees e LEFT JOIN employees m ON m.id = e.manager_id"])

P("everyone-under-them", "Everyone Under Them", "recursive", "hierarchies", "hard",
  """
  A manager's **reports** are the people who report to them directly, plus everyone who reports to those people, and so
  on down.

  For every employee who has at least one report, return `name` and `reports` (how many reports they have in total),
  in any order.
  """,
  [EMPLOYEES],
  """
  WITH RECURSIVE chain(boss, report) AS (
    SELECT manager_id, id FROM employees WHERE manager_id IS NOT NULL
    UNION ALL
    SELECT c.boss, e.id FROM chain c JOIN employees e ON e.manager_id = c.report
  )
  SELECT e.name, COUNT(*) AS reports
  FROM chain c
  JOIN employees e ON e.id = c.boss
  GROUP BY c.boss, e.name
  """,
  [(EMP_EX, "Everyone else sits under Ava: 4 reports. Dara and Elif report to Bilal: 2. Chen manages nobody.")],
  lambda rng, n, k: only(staff(rng, n, k), "employees"),
  wrong=["SELECT m.name, COUNT(*) AS reports FROM employees e JOIN employees m ON m.id = e.manager_id GROUP BY m.id, m.name",
         "WITH RECURSIVE chain(boss, report) AS (SELECT manager_id, id FROM employees WHERE manager_id IS NOT NULL UNION SELECT c.boss, e.id FROM chain c JOIN employees e ON e.manager_id = c.report) SELECT e.name, COUNT(*) + 1 AS reports FROM chain c JOIN employees e ON e.id = c.boss GROUP BY c.boss, e.name"])

DAILY = T("daily_sales", ("day", "TEXT", "pk"), ("revenue", "INTEGER"))


def gappy_gen(rng, n, k):
    rows, d = [], rng.randint(0, 200)
    for _ in range(n + 1):
        rows.append((day(d), rng.randint(1, 500)))
        d += 1 if rng.random() < 0.6 else rng.randint(2, 5)
    return {"daily_sales": rows}

P("fill-the-calendar", "Fill the Calendar", "recursive", "series", "medium",
  """
  `daily_sales` skips days with no sales. A chart needs **every day** from the first logged day to the last one.

  Return `day` and `revenue` for every day in that range, using `0` for days that aren't in the table. Order by `day`.
  """,
  [DAILY],
  """
  WITH RECURSIVE days(day) AS (
    SELECT MIN(day) FROM daily_sales
    UNION ALL
    SELECT date(day, '+1 day') FROM days WHERE day < (SELECT MAX(day) FROM daily_sales)
  )
  SELECT d.day, COALESCE(s.revenue, 0) AS revenue
  FROM days d
  LEFT JOIN daily_sales s ON s.day = d.day
  ORDER BY d.day
  """,
  [({"daily_sales": [("2024-02-27", 40), ("2024-02-28", 15), ("2024-03-02", 60)]},
    "2024 is a leap year, so February 29 and March 1 are missing in between; both show 0.")],
  gappy_gen,
  ordered=True,
  wrong=["SELECT day, revenue FROM daily_sales ORDER BY day",
         "WITH RECURSIVE days(day) AS (SELECT MIN(day) FROM daily_sales UNION ALL SELECT date(day, '+1 day') FROM days WHERE day < (SELECT MAX(day) FROM daily_sales)) SELECT d.day, s.revenue FROM days d LEFT JOIN daily_sales s ON s.day = d.day ORDER BY d.day"],
  notes="`date('2024-02-28', '+1 day')` gives `'2024-02-29'`. A recursive query keeps adding rows until its `WHERE` stops it.")

# --- Gaps & islands -------------------------------------------------------------------------------

LOGINS = T("logins", ("user_id", "INTEGER"), ("login_on", "TEXT"))

P("longest-streak", "Longest Login Streak", "gaps-islands", "streaks", "hard",
  """
  A **streak** is a run of consecutive calendar days on which a user logged in. Some users logged in more than once on
  the same day.

  Return `user_id` and `streak` (the length of their longest streak, in days) for every user who has logged in, in any
  order.
  """,
  [LOGINS],
  """
  WITH days AS (
    SELECT DISTINCT user_id, login_on FROM logins
  ),
  grouped AS (
    SELECT user_id,
           julianday(login_on) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_on) AS grp
    FROM days
  ),
  runs AS (
    SELECT user_id, COUNT(*) AS len FROM grouped GROUP BY user_id, grp
  )
  SELECT user_id, MAX(len) AS streak FROM runs GROUP BY user_id
  """,
  [({"logins": [(1, "2024-01-01"), (1, "2024-01-02"), (1, "2024-01-02"), (1, "2024-01-03"), (1, "2024-01-05"), (2, "2024-01-04"), (2, "2024-01-06")]},
    "User 1 logged in January 1, 2 (twice) and 3: a 3-day streak, then January 5 on its own. User 2 never logged in two days running.")],
  lambda rng, n, k: only(app(rng, n * 2, k), "logins"),
  wrong=["WITH grouped AS (SELECT user_id, julianday(login_on) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_on) AS grp FROM logins), runs AS (SELECT user_id, COUNT(*) AS len FROM grouped GROUP BY user_id, grp) SELECT user_id, MAX(len) AS streak FROM runs GROUP BY user_id",
         "SELECT user_id, COUNT(DISTINCT login_on) AS streak FROM logins GROUP BY user_id"],
  notes="Within a streak, the date and the row number both go up by one each day, so their difference stays the same. That difference names the streak.")

SEATS = T("seats", ("id", "INTEGER", "pk"), ("free", "INTEGER"))


def seats_gen(rng, n, k):
    p = 0.6 if ties(k) else 0.75
    return {"seats": [(i + 1, 1 if rng.random() < p else 0) for i in range(n + 6)]}

P("three-free-seats", "Three Free Seats in a Row", "gaps-islands", "streaks", "medium",
  """
  Seats in a row are numbered `1, 2, 3…` with no gaps, and `free` is `1` for an empty seat. A group of three wants to sit
  together.

  Return the `id` of every free seat that is part of a run of **at least 3** free seats side by side, ordered by `id`.
  """,
  [SEATS],
  """
  WITH f AS (
    SELECT id, id - ROW_NUMBER() OVER (ORDER BY id) AS grp FROM seats WHERE free = 1
  )
  SELECT id FROM f
  WHERE grp IN (SELECT grp FROM f GROUP BY grp HAVING COUNT(*) >= 3)
  ORDER BY id
  """,
  [({"seats": [(1, 1), (2, 1), (3, 0), (4, 1), (5, 1), (6, 1), (7, 1), (8, 0), (9, 1)]},
    "Seats 4 to 7 are four free seats in a row. Seats 1 and 2 are only two, and seat 9 is alone.")],
  seats_gen,
  ordered=True,
  wrong=["SELECT id FROM (SELECT id, free, LAG(free) OVER (ORDER BY id) AS p, LEAD(free) OVER (ORDER BY id) AS q FROM seats) WHERE free = 1 AND (p = 1 OR q = 1) ORDER BY id",
         "SELECT id FROM (SELECT id, free, LAG(free) OVER (ORDER BY id) AS p, LEAD(free) OVER (ORDER BY id) AS q FROM seats) WHERE free = 1 AND p = 1 AND q = 1 ORDER BY id"],
  sizes=[1, 2, 4, 6, 8, 10, 14, 20, 30, 45, 70, 120])

EVENTS = T("events", ("user_id", "INTEGER"), ("at", "TEXT"))


def events_gen(rng, n, k):
    rows = []
    for u in range(1, max(1, n // 4 + 1) + 1):
        t = rng.randint(0, 600)
        for _ in range(rng.randint(1, max(1, n // 2))):
            rows.append((u, f"2024-05-{1 + t // 1440:02d} {t % 1440 // 60:02d}:{t % 60:02d}"))
            t += rng.choice([5, 30, 31, 45]) if ties(k) else rng.choice([rng.randint(1, 30), rng.randint(31, 300)])
    rng.shuffle(rows)
    return {"events": rows}

P("browsing-sessions", "Browsing Sessions", "gaps-islands", "sessions", "hard",
  """
  Each row of `events` is a page view at minute precision. A user's views belong to the same **session** until there's
  a gap of **more than 30 minutes**; the next view then starts a new session. (A gap of exactly 30 minutes stays in the
  same session.)

  Return `user_id` and `sessions` (how many sessions they had), in any order.
  """,
  [EVENTS],
  """
  WITH gaps AS (
    SELECT user_id,
           (strftime('%s', at) - strftime('%s', LAG(at) OVER (PARTITION BY user_id ORDER BY at))) / 60 AS gap
    FROM events
  )
  SELECT user_id, SUM(CASE WHEN gap IS NULL OR gap > 30 THEN 1 ELSE 0 END) AS sessions
  FROM gaps
  GROUP BY user_id
  """,
  [({"events": [(1, "2024-05-01 09:00"), (1, "2024-05-01 09:20"), (1, "2024-05-01 09:50"), (1, "2024-05-01 10:30"), (2, "2024-05-01 12:00")]},
    "User 1's view at 9:50 comes exactly 30 minutes after 9:20, so it continues the session; 10:30 is 40 minutes later and starts a second one.")],
  events_gen,
  wrong=["WITH gaps AS (SELECT user_id, (strftime('%s', at) - strftime('%s', LAG(at) OVER (PARTITION BY user_id ORDER BY at))) / 60 AS gap FROM events) SELECT user_id, SUM(CASE WHEN gap IS NULL OR gap >= 30 THEN 1 ELSE 0 END) AS sessions FROM gaps GROUP BY user_id",
         "WITH gaps AS (SELECT user_id, (strftime('%s', at) - strftime('%s', LAG(at) OVER (ORDER BY at))) / 60 AS gap FROM events) SELECT user_id, SUM(CASE WHEN gap IS NULL OR gap > 30 THEN 1 ELSE 0 END) AS sessions FROM gaps GROUP BY user_id"],
  notes="`strftime('%s', at)` is the time in whole seconds, so differences are exact. (Differences of `julianday()` values are fractions of a day and can be a hair off.)")

INVOICES = T("invoices", ("no", "INTEGER", "pk"))


def invoices_gen(rng, n, k):
    no, rows = rng.randint(100, 900), []
    for _ in range(n + 1):
        rows.append((no,))
        no += 1 if rng.random() < 0.65 else rng.randint(2, 6)
    return {"invoices": rows}

P("missing-invoices", "Missing Invoice Numbers", "gaps-islands", "missing-ranges", "medium",
  """
  Invoice numbers should run without gaps, but some are missing. Between the smallest and the largest number in the
  table, find every **range of missing numbers**.

  Return `gap_start` and `gap_end` (the first and last missing number of each range), ordered by `gap_start`.
  """,
  [INVOICES],
  """
  SELECT no + 1 AS gap_start, next_no - 1 AS gap_end
  FROM (SELECT no, LEAD(no) OVER (ORDER BY no) AS next_no FROM invoices)
  WHERE next_no - no > 1
  ORDER BY gap_start
  """,
  [({"invoices": [(101,), (102,), (105,), (106,), (110,)]}, "103–104 and 107–109 are missing.")],
  invoices_gen,
  ordered=True,
  wrong=["SELECT no + 1 AS gap_start, next_no AS gap_end FROM (SELECT no, LEAD(no) OVER (ORDER BY no) AS next_no FROM invoices) WHERE next_no - no > 1 ORDER BY gap_start",
         "SELECT no AS gap_start, next_no AS gap_end FROM (SELECT no, LEAD(no) OVER (ORDER BY no) AS next_no FROM invoices) WHERE next_no - no > 1 ORDER BY gap_start"],
  sizes=[2, 3, 4, 6, 8, 12, 16, 24, 36, 60, 100, 160])

# --- Reporting -------------------------------------------------------------------------------------

QSALES = T("quarter_sales", ("rep", "TEXT"), ("quarter", "TEXT"), ("amount", "INTEGER"))


def qsales_gen(rng, n, k):
    reps = firsts(rng, max(1, n // 3 + 1))
    return {"quarter_sales": [(rng.choice(reps), rng.choice(["Q1", "Q2", "Q3", "Q4"]), rng.choice([10, 20]) if ties(k) else rng.randint(1, 300)) for _ in range(n)]}

P("quarterly-pivot", "Quarterly Pivot", "reporting", "pivot", "medium",
  """
  `quarter_sales` has one row per sale, with the `quarter` written `'Q1'` to `'Q4'`. Finance wants one row per rep and
  one column per quarter.

  Return `rep`, `q1`, `q2`, `q3` and `q4`: the rep's total in each quarter, `0` where they sold nothing. Order by `rep`.
  """,
  [QSALES],
  """
  SELECT rep,
         SUM(CASE WHEN quarter = 'Q1' THEN amount ELSE 0 END) AS q1,
         SUM(CASE WHEN quarter = 'Q2' THEN amount ELSE 0 END) AS q2,
         SUM(CASE WHEN quarter = 'Q3' THEN amount ELSE 0 END) AS q3,
         SUM(CASE WHEN quarter = 'Q4' THEN amount ELSE 0 END) AS q4
  FROM quarter_sales
  GROUP BY rep
  ORDER BY rep
  """,
  [({"quarter_sales": [("Lena", "Q1", 120), ("Kai", "Q2", 80), ("Lena", "Q1", 30), ("Lena", "Q4", 50)]},
    "Lena sold twice in Q1 (150 in total) and once in Q4. Kai only sold in Q2.")],
  qsales_gen,
  ordered=True,
  wrong=["SELECT rep, MAX(CASE WHEN quarter = 'Q1' THEN amount ELSE 0 END) AS q1, MAX(CASE WHEN quarter = 'Q2' THEN amount ELSE 0 END) AS q2, MAX(CASE WHEN quarter = 'Q3' THEN amount ELSE 0 END) AS q3, MAX(CASE WHEN quarter = 'Q4' THEN amount ELSE 0 END) AS q4 FROM quarter_sales GROUP BY rep ORDER BY rep",
         "SELECT rep, SUM(CASE WHEN quarter = 'Q1' THEN amount END) AS q1, SUM(CASE WHEN quarter = 'Q2' THEN amount END) AS q2, SUM(CASE WHEN quarter = 'Q3' THEN amount END) AS q3, SUM(CASE WHEN quarter = 'Q4' THEN amount END) AS q4 FROM quarter_sales GROUP BY rep ORDER BY rep"])

LOGINS_U = T("logins", ("user_id", "INTEGER", "fk users.id"), ("login_on", "TEXT"))


def retention_gen(rng, n, k):
    d = app(rng, n * 2, k, days=max(4, n // 2))
    # Make sure some people come back the very next day.
    for uid, _, _, signed in d["users"]:
        if rng.random() < 0.4:
            d["logins"].append((uid, (datetime.date.fromisoformat(signed) + datetime.timedelta(days=1)).isoformat()))
    return d

P("came-back-next-day", "Came Back the Next Day", "reporting", "retention", "medium",
  """
  Product wants to know how many new users return on the **day after they sign up**. Group users by the day they
  signed up.

  Return `signed_up`, `signups` (users who signed up that day) and `returned` (how many of them logged in on the
  following day), ordered by `signed_up`. A user who logged in several times that day still counts once.
  """,
  [USERS, LOGINS_U],
  """
  SELECT u.signed_up,
         COUNT(*) AS signups,
         SUM(EXISTS (SELECT 1 FROM logins l WHERE l.user_id = u.id AND l.login_on = date(u.signed_up, '+1 day'))) AS returned
  FROM users u
  GROUP BY u.signed_up
  ORDER BY u.signed_up
  """,
  [({"users": [(1, "Ava Moss", "BR", "2024-01-01"), (2, "Bilal Cruz", "CA", "2024-01-01"), (3, "Chen Ito", "DE", "2024-01-02")],
     "logins": [(1, "2024-01-02"), (1, "2024-01-02"), (2, "2024-01-03"), (3, "2024-01-03")]},
    "Of the two January 1 signups, only Ava logged in on January 2 (twice, but she counts once). Chen came back on January 3, the day after he joined.")],
  retention_gen,
  ordered=True,
  wrong=["SELECT u.signed_up, COUNT(*) AS signups, COUNT(l.user_id) AS returned FROM users u LEFT JOIN logins l ON l.user_id = u.id AND l.login_on = date(u.signed_up, '+1 day') GROUP BY u.signed_up ORDER BY u.signed_up",
         "SELECT u.signed_up, COUNT(*) AS signups, SUM(EXISTS (SELECT 1 FROM logins l WHERE l.user_id = u.id AND l.login_on > u.signed_up)) AS returned FROM users u GROUP BY u.signed_up ORDER BY u.signed_up"])

MEDIAN_EX = {"employees": EMP_EX["employees"] + [(6, "Fern Lund", 2, 2, 75000, "2023-02-01")]}

P("median-salary", "Median Salary by Department", "reporting", "median-percentile", "hard",
  """
  The **median** is the middle salary once a department's salaries are sorted; with an even number of people, it's the
  average of the two in the middle.

  Return `dept_id` and `median` (rounded to 2 decimal places) for every department with employees, in any order.
  Employees without a department are left out.
  """,
  [EMPLOYEES],
  """
  WITH ranked AS (
    SELECT dept_id, salary,
           ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary) AS rn,
           COUNT(*) OVER (PARTITION BY dept_id) AS cnt
    FROM employees
    WHERE dept_id IS NOT NULL
  )
  SELECT dept_id, ROUND(AVG(salary), 2) AS median
  FROM ranked
  WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2)
  GROUP BY dept_id
  """,
  [(MEDIAN_EX, "Department 2's salaries sorted are 48,000, 61,000 and 75,000: the median is 61,000. Department 1 has two people, so its median is the average of 60,000 and 96,000: 78,000.")],
  lambda rng, n, k: only(staff(rng, n, k), "employees"),
  wrong=["SELECT dept_id, ROUND(AVG(salary), 2) AS median FROM employees WHERE dept_id IS NOT NULL GROUP BY dept_id",
         "WITH ranked AS (SELECT dept_id, salary, ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary) AS rn, COUNT(*) OVER (PARTITION BY dept_id) AS cnt FROM employees WHERE dept_id IS NOT NULL) SELECT dept_id, ROUND(AVG(salary), 2) AS median FROM ranked WHERE rn = (cnt + 1) / 2 GROUP BY dept_id"],
  notes="In SQLite, `(cnt + 1) / 2` is whole-number division: for 4 people it's 2, and `(cnt + 2) / 2` is 3.")

ACCOUNTS = T("accounts", ("id", "INTEGER", "pk"), ("email", "TEXT"))


def dup_emails_gen(rng, n, k):
    pool = [f"{f.lower()}@mail.test" for f in FIRST[: max(3, n // 2 + 2)]]
    return {"accounts": [(i + 1, rng.choice(pool)) for i in range(n + 1)]}

P("duplicate-emails", "Duplicate Emails", "reporting", "dedup", "easy",
  """
  Some people created more than one account with the same email.

  Return every `email` used by **more than one** account, each once, in alphabetical order.
  """,
  [ACCOUNTS],
  "SELECT email FROM accounts GROUP BY email HAVING COUNT(*) > 1 ORDER BY email",
  [({"accounts": [(1, "nia@mail.test"), (2, "omar@mail.test"), (3, "nia@mail.test"), (4, "pia@mail.test"), (5, "nia@mail.test")]},
    "Nia's email is on three accounts. Omar's and Pia's are used once each.")],
  dup_emails_gen,
  ordered=True,
  wrong=["SELECT DISTINCT email FROM accounts ORDER BY email",
         "SELECT email FROM accounts GROUP BY email HAVING COUNT(*) > 2 ORDER BY email"])

SIGNUPS = T("signups", ("id", "INTEGER", "pk"), ("email", "TEXT"), ("signed_at", "TEXT"))


def signups_gen(rng, n, k):
    pool = [f"{f.lower()}@mail.test" for f in FIRST[: max(2, n // 2 + 1)]]
    ids = list(range(1, n + 2))
    rng.shuffle(ids)
    rows = [(i, rng.choice(pool), f"{day(rng.randint(0, 3 if ties(k) else 60))} {rng.randint(8, 20):02d}:00") for i in ids]
    return {"signups": rows}

P("first-signup", "Keep the First Sign-up", "reporting", "dedup", "medium",
  """
  Some emails signed up several times. Keep only each email's **first** sign-up: the earliest `signed_at`, and if two
  share that time, the smaller `id`. (Ids weren't handed out in time order.)

  Return `id`, `email` and `signed_at` of the rows to keep, ordered by `id`.
  """,
  [SIGNUPS],
  """
  SELECT id, email, signed_at
  FROM (
    SELECT id, email, signed_at,
           ROW_NUMBER() OVER (PARTITION BY email ORDER BY signed_at, id) AS rn
    FROM signups
  )
  WHERE rn = 1
  ORDER BY id
  """,
  [({"signups": [(1, "kai@mail.test", "2024-02-03 10:00"), (2, "lena@mail.test", "2024-02-01 09:00"), (3, "kai@mail.test", "2024-01-30 18:00"), (4, "lena@mail.test", "2024-02-01 09:00")]},
    "Kai's first sign-up is row 3, even though row 1 has a smaller id. Lena's two sign-ups have the same time, so the smaller id, 2, is kept.")],
  signups_gen,
  ordered=True,
  wrong=["SELECT MIN(id) AS id, email, MIN(signed_at) AS signed_at FROM signups GROUP BY email ORDER BY id",
         "SELECT id, email, signed_at FROM (SELECT id, email, signed_at, ROW_NUMBER() OVER (PARTITION BY email ORDER BY signed_at DESC, id) AS rn FROM signups) WHERE rn = 1 ORDER BY id"])

done()
