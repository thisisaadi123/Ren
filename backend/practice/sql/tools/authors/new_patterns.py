"""New patterns in existing topics: range joins, as-of lookups, string aggregation, first/last/Nth value,
counts beside each row, and following links."""
import _common  # noqa: F401
from _common import only
from _examples import EMP_EX, SHOP_EX
from author import P, T, day, done, firsts, names
from worlds import EMPLOYEES, ORDER_ITEMS, ORDERS, PRODUCTS, shop, staff, ties

ex = lambda data, *tables: only(data, *tables)  # noqa: E731

# --- Joining on a range ----------------------------------------------------------------------------

PRICES = T("prices", ("product_id", "INTEGER"), ("start_day", "TEXT"), ("end_day", "TEXT"), ("price", "REAL"))
SALES = T("sales", ("product_id", "INTEGER"), ("sold_on", "TEXT"), ("units", "INTEGER"))


def prices_gen(rng, n, k):
    prices, sales = [], []
    for pid in range(1, max(1, n // 3) + 2):
        d = 0
        for _ in range(rng.randint(1, 3)):
            length = rng.randint(3, 15)
            prices.append((pid, day(d), day(d + length - 1), rng.choice([5.0, 10.0]) if ties(k) else round(rng.uniform(2, 50), 2)))
            d += length
        if rng.random() < 0.8:
            for _ in range(rng.randint(1, 4)):
                sales.append((pid, day(rng.randint(0, d - 1)), rng.randint(1, 9)))
    return {"prices": prices, "sales": sales}

P("average-selling-price", "Average Selling Price", "joins", "range-join", "medium",
  """
  A product's price changes over time: each row of `prices` holds from `start_day` to `end_day` (both included), and a
  product's periods never overlap. Each sale was made at the price in force on `sold_on`.

  For every product in `prices`, return `product_id` and `avg_price`: total money taken divided by units sold, rounded
  to 2 decimal places, or `0` if it never sold. Any order.
  """,
  [PRICES, SALES],
  """
  SELECT p.product_id,
         COALESCE(ROUND(SUM(s.units * p.price) / SUM(s.units), 2), 0) AS avg_price
  FROM prices p
  LEFT JOIN sales s ON s.product_id = p.product_id AND s.sold_on BETWEEN p.start_day AND p.end_day
  GROUP BY p.product_id
  """,
  [({"prices": [(1, "2024-02-01", "2024-02-10", 5.0), (1, "2024-02-11", "2024-02-29", 8.0), (2, "2024-02-01", "2024-02-29", 20.0)],
     "sales": [(1, "2024-02-05", 10), (1, "2024-02-12", 5)]},
    "Product 1 sold 10 units at 5 and 5 units at 8: 90 / 15 = 6.00. Product 2 never sold.")],
  prices_gen,
  wrong=["SELECT p.product_id, COALESCE(ROUND(SUM(s.units * p.price) / SUM(s.units), 2), 0) AS avg_price FROM prices p LEFT JOIN sales s ON s.product_id = p.product_id GROUP BY p.product_id",
         "SELECT p.product_id, ROUND(SUM(s.units * p.price) / SUM(s.units), 2) AS avg_price FROM prices p JOIN sales s ON s.product_id = p.product_id AND s.sold_on BETWEEN p.start_day AND p.end_day GROUP BY p.product_id"])

TIERS = T("tiers", ("min_kg", "REAL"), ("max_kg", "REAL"), ("fee", "REAL"))
PARCELS = T("parcels", ("id", "INTEGER", "pk"), ("kg", "REAL"))
TIER_ROWS = [(0.0, 1.0, 4.5), (1.0, 5.0, 7.0), (5.0, 20.0, 12.0), (20.0, None, 30.0)]


def parcels_gen(rng, n, k):
    return {"tiers": TIER_ROWS, "parcels": [(i + 1, rng.choice([1.0, 5.0, 20.0, 0.5]) if ties(k) else round(rng.uniform(0.1, 40), 1)) for i in range(n + 1)]}

P("shipping-tiers", "Shipping Tiers", "joins", "range-join", "medium",
  """
  Shipping fees depend on weight. A parcel falls in the tier where `min_kg ≤ kg < max_kg`; the heaviest tier has no
  upper limit (`max_kg` is NULL).

  Return each parcel's `id` and its `fee`, in any order.
  """,
  [TIERS, PARCELS],
  "SELECT p.id, t.fee FROM parcels p JOIN tiers t ON p.kg >= t.min_kg AND (t.max_kg IS NULL OR p.kg < t.max_kg)",
  [({"tiers": TIER_ROWS, "parcels": [(1, 0.4), (2, 5.0), (3, 26.0)]},
    "Parcel 2 weighs exactly 5 kg, so it's in the 5–20 tier (12.00), not the 1–5 tier. Parcel 3 is in the open-ended top tier.")],
  parcels_gen,
  wrong=["SELECT p.id, t.fee FROM parcels p JOIN tiers t ON p.kg BETWEEN t.min_kg AND t.max_kg",
         "SELECT p.id, t.fee FROM parcels p JOIN tiers t ON p.kg >= t.min_kg AND p.kg < t.max_kg"],
  notes="`BETWEEN` includes both ends, so a weight on a boundary would match two tiers.")

# --- Value as of a date ------------------------------------------------------------------------------

PRICE_LOG = T("price_log", ("product_id", "INTEGER"), ("changed_on", "TEXT"), ("new_price", "REAL"))
ITEMS = T("items", ("id", "INTEGER", "pk"), ("name", "TEXT"))


def price_log_gen(rng, n, k):
    items = [(i + 1, nm) for i, nm in enumerate(firsts(rng, max(1, n // 2 + 1)))]
    log = []
    for i, _ in items:
        days = rng.sample(range(0, 40), rng.randint(0, 4))
        for d in days:
            log.append((i, day(d, (2024, 8, 1)), round(rng.uniform(5, 60), 2)))
    if ties(k):
        log.append((1, "2024-08-16", 11.0))
    return {"items": items, "price_log": log}

P("price-on-the-day", "Price on the Day", "subqueries", "as-of-lookup", "medium",
  """
  Every product started at a price of **10**. `price_log` records each later change. Find what each product cost on
  **2024-08-16**: its most recent change on or before that day, or 10 if it hadn't changed yet.

  Return every item's `id` and `price`, in any order.
  """,
  [ITEMS, PRICE_LOG],
  """
  SELECT i.id,
         COALESCE((SELECT l.new_price FROM price_log l
                   WHERE l.product_id = i.id AND l.changed_on <= '2024-08-16'
                   ORDER BY l.changed_on DESC LIMIT 1), 10) AS price
  FROM items i
  """,
  [({"items": [(1, "Teapot"), (2, "Whisk"), (3, "Kite")],
     "price_log": [(1, "2024-08-14", 20.0), (1, "2024-08-16", 35.0), (1, "2024-08-18", 25.0), (2, "2024-08-17", 15.0)]},
    "The Teapot's last change by August 16 is on the 16th itself: 35. The Whisk only changed on the 17th, so it's still 10, and the Kite never changed.")],
  price_log_gen,
  wrong=["SELECT i.id, COALESCE((SELECT MAX(l.new_price) FROM price_log l WHERE l.product_id = i.id AND l.changed_on <= '2024-08-16'), 10) AS price FROM items i",
         "SELECT i.id, COALESCE((SELECT l.new_price FROM price_log l WHERE l.product_id = i.id AND l.changed_on < '2024-08-16' ORDER BY l.changed_on DESC LIMIT 1), 10) AS price FROM items i"])

RATES = T("rates", ("currency", "TEXT"), ("valid_from", "TEXT"), ("rate", "REAL"))
FX_ORDERS = T("fx_orders", ("id", "INTEGER", "pk"), ("currency", "TEXT"), ("ordered_on", "TEXT"), ("amount", "REAL"))


def fx_gen(rng, n, k):
    rates = []
    for c, base in [("EUR", 1.1), ("GBP", 1.3), ("JPY", 0.007)]:
        for d in sorted(rng.sample(range(2, 60), rng.randint(1, 4))):
            rates.append((c, day(d, (2024, 3, 1)), round(base * rng.uniform(0.95, 1.05), 4)))
    orders = [(i + 1, rng.choice(["EUR", "GBP", "JPY"]), day(rng.randint(0, 65), (2024, 3, 1)), round(rng.uniform(5, 500), 2)) for i in range(n + 1)]
    return {"rates": rates, "fx_orders": orders}

P("amounts-in-dollars", "Amounts in Dollars", "subqueries", "as-of-lookup", "hard",
  """
  `rates` gives each currency's dollar rate from `valid_from` onward, until its next row. Convert every order to dollars
  using the rate in force on `ordered_on` (a rate starting that very day counts). An order placed before its currency's
  first rate can't be converted: NULL.

  Return `id` and `usd` (`amount × rate`, rounded to 2 decimal places), in any order.
  """,
  [RATES, FX_ORDERS],
  """
  SELECT o.id,
         ROUND(o.amount * (SELECT r.rate FROM rates r
                           WHERE r.currency = o.currency AND r.valid_from <= o.ordered_on
                           ORDER BY r.valid_from DESC LIMIT 1), 2) AS usd
  FROM fx_orders o
  """,
  [({"rates": [("EUR", "2024-03-03", 1.08), ("EUR", "2024-03-10", 1.1)],
     "fx_orders": [(1, "EUR", "2024-03-01", 100.0), (2, "EUR", "2024-03-10", 100.0), (3, "EUR", "2024-03-09", 50.0)]},
    "Order 1 came before any EUR rate: NULL. Order 2 uses the rate that starts that day (1.10). Order 3 uses 1.08.")],
  fx_gen,
  wrong=["SELECT o.id, ROUND(o.amount * (SELECT r.rate FROM rates r WHERE r.currency = o.currency ORDER BY r.valid_from DESC LIMIT 1), 2) AS usd FROM fx_orders o",
         "SELECT o.id, ROUND(o.amount * (SELECT r.rate FROM rates r WHERE r.currency = o.currency AND r.valid_from < o.ordered_on ORDER BY r.valid_from DESC LIMIT 1), 2) AS usd FROM fx_orders o"])

# --- Joining strings in a group -------------------------------------------------------------------------

P("category-product-lists", "Category Product Lists", "strings-dates", "string-aggregation", "easy",
  """
  For each category, list its products in one line: names in alphabetical order, separated by a comma and a space.

  Return `category` and `products`, ordered by `category`.
  """,
  [PRODUCTS],
  "SELECT category, GROUP_CONCAT(name, ', ' ORDER BY name) AS products FROM products GROUP BY category ORDER BY category",
  [(ex(SHOP_EX, "products"), "Books has the Comic and the Novel, so it reads `Comic, Novel`.")],
  lambda rng, n, k: only(shop(rng, n * 2, k), "products"),
  ordered=True,
  wrong=["SELECT category, GROUP_CONCAT(name, ', ') AS products FROM products GROUP BY category ORDER BY category",
         "SELECT category, GROUP_CONCAT(name ORDER BY name) AS products FROM products GROUP BY category ORDER BY category"],
  notes="`GROUP_CONCAT(x, sep ORDER BY y)` joins a group's values in that order. Without `ORDER BY`, the order isn't guaranteed.")

P("sold-each-day", "Sold Each Day", "strings-dates", "string-aggregation", "medium",
  """
  For each day with orders (any status), return `ordered_on`, `products` (how many **different** products were in that
  day's orders) and `names` (those products' names, each once, in alphabetical order, separated by commas without
  spaces). Order by `ordered_on`.
  """,
  [PRODUCTS, ORDERS, ORDER_ITEMS],
  """
  SELECT o.ordered_on,
         COUNT(DISTINCT p.name) AS products,
         GROUP_CONCAT(DISTINCT p.name ORDER BY p.name) AS names
  FROM orders o
  JOIN order_items i ON i.order_id = o.id
  JOIN products p ON p.id = i.product_id
  GROUP BY o.ordered_on
  ORDER BY o.ordered_on
  """,
  [({"products": SHOP_EX["products"], "orders": [(1, 1, "2024-01-03", "delivered"), (2, 2, "2024-01-03", "cancelled"), (3, 1, "2024-01-04", "delivered")],
     "order_items": [(1, 1, 2), (1, 2, 1), (2, 2, 1), (2, 3, 3), (3, 4, 2)]},
    "On January 3, two orders hold a Kettle, a Novel (in both) and a Kite: three products. January 4 only has Comics.")],
  lambda rng, n, k: only(shop(rng, n, k, span=max(2, n // 3)), "products", "orders", "order_items"),
  ordered=True,
  wrong=["SELECT o.ordered_on, COUNT(p.name) AS products, GROUP_CONCAT(p.name) AS names FROM orders o JOIN order_items i ON i.order_id = o.id JOIN products p ON p.id = i.product_id GROUP BY o.ordered_on ORDER BY o.ordered_on",
         "SELECT o.ordered_on, COUNT(DISTINCT p.name) AS products, GROUP_CONCAT(DISTINCT p.name) AS names FROM orders o JOIN order_items i ON i.order_id = o.id JOIN products p ON p.id = i.product_id GROUP BY o.ordered_on ORDER BY o.ordered_on"])

# --- First, last and Nth value -----------------------------------------------------------------------------

DAILY = T("daily_sales", ("day", "TEXT", "pk"), ("revenue", "INTEGER"))

P("vs-first-of-month", "Against the First of the Month", "window-aggregates", "first-last-value", "medium",
  """
  `daily_sales` has one row per day (days can be missing). Compare each day with the **first day recorded in its
  month**.

  Return `day`, `revenue` and `first_revenue` (the revenue of the earliest recorded day in the same month), ordered by
  `day`.
  """,
  [DAILY],
  """
  SELECT day, revenue,
         FIRST_VALUE(revenue) OVER (PARTITION BY strftime('%Y-%m', day) ORDER BY day) AS first_revenue
  FROM daily_sales
  ORDER BY day
  """,
  [({"daily_sales": [("2024-01-30", 50), ("2024-01-31", 70), ("2024-02-02", 40), ("2024-02-05", 90)]},
    "February's first recorded day is the 2nd (40), so February 5 is compared with 40, not with January's 50.")],
  lambda rng, n, k: {"daily_sales": [(day(d, (2024, 1, 1)), rng.randint(0, 300)) for d in sorted(rng.sample(range(0, 400), n + 1))]},
  ordered=True,
  wrong=["SELECT day, revenue, FIRST_VALUE(revenue) OVER (ORDER BY day) AS first_revenue FROM daily_sales ORDER BY day",
         "SELECT day, revenue, LAG(revenue) OVER (PARTITION BY strftime('%Y-%m', day) ORDER BY day) AS first_revenue FROM daily_sales ORDER BY day"])

TRADES = T("trades", ("id", "INTEGER", "pk"), ("symbol", "TEXT"), ("at", "TEXT"), ("price", "REAL"))


def trades_gen(rng, n, k):
    rows, seen = [], set()
    for i in range(n + 1):
        sym, d = rng.choice(["ACME", "BOLT", "CRUX"]), rng.randint(0, max(1, n // 6))
        while True:
            t = rng.randint(9 * 60, 16 * 60)
            if (sym, d, t) not in seen:
                seen.add((sym, d, t))
                break
        rows.append((i + 1, sym, f"{day(d, (2024, 6, 3))} {t // 60:02d}:{t % 60:02d}", round(rng.uniform(10, 20), 2)))
    rng.shuffle(rows)
    return {"trades": rows}

P("open-and-close", "Open and Close", "window-aggregates", "first-last-value", "hard",
  """
  `trades` records each trade's `symbol`, time `at` (`YYYY-MM-DD HH:MM`) and `price`; no symbol trades twice in the same
  minute. For each symbol and day, the **open** is the day's first trade price and the **close** is its last.

  Return `symbol`, `day` (`YYYY-MM-DD`), `open` and `close`, ordered by `symbol`, then `day`.
  """,
  [TRADES],
  """
  SELECT DISTINCT symbol, date(at) AS day,
         FIRST_VALUE(price) OVER w AS open,
         LAST_VALUE(price) OVER w AS close
  FROM trades
  WINDOW w AS (PARTITION BY symbol, date(at) ORDER BY at ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
  ORDER BY symbol, day
  """,
  [({"trades": [(1, "ACME", "2024-06-03 09:30", 12.0), (2, "ACME", "2024-06-03 15:55", 12.8), (3, "ACME", "2024-06-03 11:10", 11.5), (4, "BOLT", "2024-06-03 10:00", 30.0)]},
    "ACME opened at 12.00 (09:30) and closed at 12.80 (15:55); the 11:10 trade is in between. BOLT traded once, so its open is its close.")],
  trades_gen,
  ordered=True,
  wrong=["SELECT DISTINCT symbol, date(at) AS day, FIRST_VALUE(price) OVER (PARTITION BY symbol, date(at) ORDER BY at) AS open, LAST_VALUE(price) OVER (PARTITION BY symbol, date(at) ORDER BY at) AS close FROM trades ORDER BY symbol, day",
         "SELECT symbol, date(at) AS day, MIN(price) AS open, MAX(price) AS close FROM trades GROUP BY symbol, day ORDER BY symbol, day"],
  notes="With `ORDER BY`, a window's frame ends at the current row by default, so `LAST_VALUE` just returns the current row. Widen the frame to `UNBOUNDED FOLLOWING`.")

RESULTS = T("results", ("event", "TEXT"), ("athlete", "TEXT"), ("seconds", "REAL"))


def results_gen(rng, n, k):
    rows = []
    for ev in ["100m", "200m", "400m"][: max(1, min(3, n // 3 + 1))]:
        for a in firsts(rng, rng.randint(1, max(2, n // 2))):
            rows.append((ev, a, rng.choice([10.0, 10.5, 11.0]) if ties(k) else round(rng.uniform(10, 13), 2)))
    return {"results": rows}

P("third-fastest", "Third-fastest Time", "window-aggregates", "first-last-value", "medium",
  """
  For each event, find the **third-fastest time**: sort the event's times from fewest seconds up and take the third
  one (equal times each take a place). An event with fewer than three results has no third time: NULL.

  Return `event` and `third`, ordered by `event`.
  """,
  [RESULTS],
  """
  SELECT DISTINCT event,
         NTH_VALUE(seconds, 3) OVER (PARTITION BY event ORDER BY seconds
                                     ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS third
  FROM results
  ORDER BY event
  """,
  [({"results": [("100m", "Ava", 10.9), ("100m", "Bea", 10.7), ("100m", "Cyrus", 10.9), ("100m", "Dev", 11.2), ("200m", "Emil", 22.0)]},
    "The 100m times in order are 10.7, 10.9, 10.9, 11.2: the third is 10.9. The 200m has only one result.")],
  results_gen,
  ordered=True,
  wrong=["SELECT DISTINCT event, NTH_VALUE(seconds, 3) OVER (PARTITION BY event ORDER BY seconds) AS third FROM results ORDER BY event",
         "SELECT DISTINCT event, NTH_VALUE(seconds, 3) OVER (PARTITION BY event ORDER BY seconds DESC ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS third FROM results ORDER BY event"])

# --- Counts beside each row ---------------------------------------------------------------------------------

POLICIES = T("policies", ("id", "INTEGER", "pk"), ("tiv_2023", "REAL"), ("tiv_2024", "REAL"), ("lat", "REAL"), ("lon", "REAL"))


def policies_gen(rng, n, k):
    spots = [(round(rng.uniform(-40, 40), 1), round(rng.uniform(-90, 90), 1)) for _ in range(max(1, n // 2 + 1))]
    values = [float(v * 10) for v in range(1, n // 2 + 3)]
    return {"policies": [(i + 1, rng.choice(values), float(rng.randint(5, 90)), *rng.choice(spots)) for i in range(n + 2)]}

P("shared-value-unique-place", "Shared Value, Unique Place", "window-aggregates", "group-counts", "hard",
  """
  An insurer wants the total 2024 value (`tiv_2024`) of the policies that meet **both** conditions:

  - their `tiv_2023` is the same as **at least one other** policy's, and
  - their location (`lat`, `lon`) is **not shared** with any other policy.

  Return one row: `total`, rounded to 2 decimal places.
  """,
  [POLICIES],
  """
  SELECT ROUND(SUM(tiv_2024), 2) AS total
  FROM (
    SELECT tiv_2024,
           COUNT(*) OVER (PARTITION BY tiv_2023) AS same_value,
           COUNT(*) OVER (PARTITION BY lat, lon) AS same_place
    FROM policies
  )
  WHERE same_value > 1 AND same_place = 1
  """,
  [({"policies": [(1, 10.0, 5.0, 10.0, 10.0), (2, 20.0, 20.0, 20.0, 20.0), (3, 10.0, 30.0, 20.0, 20.0), (4, 10.0, 40.0, 40.0, 40.0)]},
    "Policies 1, 3 and 4 share a 2023 value. Policy 3 shares its place with policy 2, so only 1 and 4 count: 5 + 40 = 45.")],
  policies_gen,
  wrong=["SELECT ROUND(SUM(tiv_2024), 2) AS total FROM (SELECT tiv_2024, COUNT(*) OVER (PARTITION BY tiv_2023) AS same_value, COUNT(*) OVER (PARTITION BY lat) AS same_place FROM policies) WHERE same_value > 1 AND same_place = 1",
         "SELECT ROUND(SUM(tiv_2024), 2) AS total FROM (SELECT tiv_2024, COUNT(*) OVER (PARTITION BY tiv_2023) AS same_value, COUNT(*) OVER (PARTITION BY lat, lon) AS same_place FROM policies) WHERE same_value >= 1 AND same_place = 1"])

P("big-team-members", "Members of Big Teams", "window-aggregates", "group-counts", "medium",
  """
  List the people who work in a department of **at least 3** employees, next to that department's size.

  Return `name`, `dept_id` and `headcount`, in any order. Employees without a department aren't in a team.
  """,
  [EMPLOYEES],
  """
  SELECT name, dept_id, headcount
  FROM (SELECT name, dept_id, COUNT(*) OVER (PARTITION BY dept_id) AS headcount FROM employees WHERE dept_id IS NOT NULL)
  WHERE headcount >= 3
  """,
  [({"employees": EMP_EX["employees"] + [(6, "Fern Lund", 2, 2, 52000, "2023-02-01")]},
    "Department 2 now has Bilal, Elif and Fern: 3 people, so all three are listed. Department 1 has only two.")],
  lambda rng, n, k: only(staff(rng, n, 1 if k % 2 else k), "employees"),
  wrong=["SELECT name, dept_id, headcount FROM (SELECT name, dept_id, COUNT(*) OVER (PARTITION BY dept_id) AS headcount FROM employees) WHERE headcount >= 3",
         "SELECT name, dept_id, headcount FROM (SELECT name, dept_id, COUNT(*) OVER () AS headcount FROM employees WHERE dept_id IS NOT NULL) WHERE headcount >= 3"])

# --- Following links ----------------------------------------------------------------------------------------

ROUTES = T("routes", ("from_stop", "TEXT"), ("to_stop", "TEXT"))
STOPS = list("ABCDEFGHJK")


def routes_gen(rng, n, k):
    stops = STOPS[: max(3, min(10, n // 2 + 3))]
    rows = set()
    for _ in range(n + 2):
        a, b = rng.sample(stops, 2)
        rows.add((a, b))
    rows.add(("A", rng.choice(stops[1:])))
    return {"routes": sorted(rows)}

P("reachable-stops", "Reachable Stops", "recursive", "graph-paths", "hard",
  """
  Each row of `routes` is a one-way bus line from `from_stop` to `to_stop`. Routes can form loops.

  Return every stop (other than `'A'` itself) that you can reach from stop `'A'` by riding one or more routes, as
  `stop`, ordered by `stop`.
  """,
  [ROUTES],
  """
  WITH RECURSIVE reach(stop) AS (
    SELECT to_stop FROM routes WHERE from_stop = 'A'
    UNION
    SELECT r.to_stop FROM reach JOIN routes r ON r.from_stop = reach.stop
  )
  SELECT stop FROM reach WHERE stop <> 'A' ORDER BY stop
  """,
  [({"routes": [("A", "B"), ("B", "C"), ("C", "A"), ("D", "E"), ("C", "D")]},
    "From A you reach B, then C, then D (from C), then E. The loop C → A doesn't add anything new.")],
  routes_gen,
  ordered=True,
  wrong=["SELECT to_stop AS stop FROM routes WHERE from_stop = 'A' AND to_stop <> 'A' ORDER BY stop",
         "SELECT DISTINCT r2.to_stop AS stop FROM routes r1 JOIN routes r2 ON r2.from_stop = r1.to_stop WHERE r1.from_stop = 'A' AND r2.to_stop <> 'A' ORDER BY stop"],
  notes="`UNION` (not `UNION ALL`) drops rows the recursion has already produced, which is what stops it going round a loop forever.")

FLIGHTS = T("flights", ("src", "TEXT"), ("dst", "TEXT"))
AIRPORTS = ["LIS", "OPO", "MAD", "BCN", "CDG", "AMS", "FRA", "OSL", "NBO", "DEN"]


def flights_gen(rng, n, k):
    ports = AIRPORTS[: max(3, min(10, n // 2 + 3))]
    rows = set()
    for _ in range(n + 2):
        a, b = rng.sample(ports, 2)
        rows.add((a, b))
    rows.add(("LIS", rng.choice(ports[1:])))
    return {"flights": sorted(rows)}

P("fewest-flights", "Fewest Flights", "recursive", "graph-paths", "hard",
  """
  `flights` lists one-way direct flights. For every airport you can reach from `'LIS'`, find the **fewest flights**
  needed to get there.

  Return `airport` and `flights`, ordered by `flights`, then `airport`. Lisbon itself isn't listed.
  """,
  [FLIGHTS],
  """
  WITH RECURSIVE hops(airport, flights) AS (
    SELECT dst, 1 FROM flights WHERE src = 'LIS'
    UNION
    SELECT f.dst, h.flights + 1
    FROM hops h JOIN flights f ON f.src = h.airport
    WHERE h.flights < (SELECT COUNT(*) FROM flights)
  )
  SELECT airport, MIN(flights) AS flights
  FROM hops
  WHERE airport <> 'LIS'
  GROUP BY airport
  ORDER BY flights, airport
  """,
  [({"flights": [("LIS", "MAD"), ("MAD", "CDG"), ("LIS", "CDG"), ("CDG", "OSL"), ("OSL", "LIS")]},
    "CDG is one flight away directly, even though LIS → MAD → CDG also works. OSL takes two: LIS → CDG → OSL.")],
  flights_gen,
  ordered=True,
  wrong=["WITH RECURSIVE hops(airport, flights) AS (SELECT dst, 1 FROM flights WHERE src = 'LIS' UNION SELECT f.dst, h.flights + 1 FROM hops h JOIN flights f ON f.src = h.airport WHERE h.flights < (SELECT COUNT(*) FROM flights)) SELECT airport, MAX(flights) AS flights FROM hops WHERE airport <> 'LIS' GROUP BY airport ORDER BY flights, airport",
         "SELECT dst AS airport, 1 AS flights FROM flights WHERE src = 'LIS' ORDER BY flights, airport"],
  notes="A path never needs more flights than there are flights in the table, so that bound stops the recursion on loops.")

done()
