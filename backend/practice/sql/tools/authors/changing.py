"""Changing Data: UPDATE, DELETE and INSERT problems, judged on the table they leave behind."""
import _common  # noqa: F401
from _common import only
from _examples import EMP_EX, SHOP_EX
from author import FIRST, P, T, day, done, maybe
from worlds import EMPLOYEES, ORDER_ITEMS, ORDERS, PRODUCTS, shop, staff, ties

ex = lambda data, *tables: only(data, *tables)  # noqa: E731

P("year-end-raises", "Year-end Raises", "changing-data", "update-rows", "easy",
  """
  Year-end raises are in: everyone in **department 2** (Sales) gets **2,500** more, and everyone in any other department
  gets **1,000** more. People without a department don't get a raise this year.

  Write one `UPDATE` on `employees`.
  """,
  [EMPLOYEES],
  """
  UPDATE employees
  SET salary = salary + CASE WHEN dept_id = 2 THEN 2500 ELSE 1000 END
  WHERE dept_id IS NOT NULL
  """,
  [(EMP_EX, "Bilal and Elif (Sales) go up by 2,500; Ava and Chen by 1,000. Dara has no department, so her salary stays 125,500.")],
  lambda rng, n, k: only(staff(rng, n, 1 if k % 2 else k), "employees"),
  wrong=["UPDATE employees SET salary = salary + CASE WHEN dept_id = 2 THEN 2500 ELSE 1000 END",
         "UPDATE employees SET salary = salary + 2500 WHERE dept_id = 2"],
  change="employees",
  notes="Without a `WHERE`, an `UPDATE` changes every row.")

SHIP = T("shipments", ("order_id", "INTEGER", "pk"), ("ordered_on", "TEXT"), ("shipped_on", "TEXT"), ("status", "TEXT"))


def ship_gen(rng, n, k):
    rows = []
    for i in range(n + 2):
        start = rng.randint(80, 100) if ties(k) else rng.randint(60, 100)
        shipped = maybe(rng, 0.5, day(start + rng.randint(0, 4)))
        rows.append((i + 1, day(start), shipped, "shipped" if shipped else "waiting"))
    return {"shipments": rows}

P("flag-late-shipments", "Flag Late Shipments", "changing-data", "update-rows", "medium",
  """
  It's **2024-04-10**. Any order that **hasn't shipped** (`shipped_on` is NULL) and was placed **more than 7 days ago**
  should have its `status` set to `'late'`. Nothing else changes.

  Write one `UPDATE` on `shipments`.
  """,
  [SHIP],
  "UPDATE shipments SET status = 'late' WHERE shipped_on IS NULL AND julianday('2024-04-10') - julianday(ordered_on) > 7",
  [({"shipments": [(1, "2024-03-28", None, "waiting"), (2, "2024-04-03", None, "waiting"), (3, "2024-03-25", "2024-03-27", "shipped"), (4, "2024-04-02", None, "waiting")]},
    "Order 1 has waited 13 days: late. Order 2 has waited exactly 7, which isn't more than 7. Order 3 has shipped. Order 4 has waited 8 days: late.")],
  ship_gen,
  wrong=["UPDATE shipments SET status = 'late' WHERE julianday('2024-04-10') - julianday(ordered_on) > 7",
         "UPDATE shipments SET status = 'late' WHERE shipped_on IS NULL AND julianday('2024-04-10') - julianday(ordered_on) >= 7"],
  change="shipments")

PRICE_CHANGES = T("price_changes", ("product_id", "INTEGER", "pk"), ("new_price", "REAL"))


def reprice_gen(rng, n, k):
    d = only(shop(rng, n * 2, k), "products")
    ids = [p[0] for p in d["products"]]
    d["price_changes"] = [(i, round(rng.uniform(2, 90), 2)) for i in rng.sample(ids, max(1, len(ids) // 2))]
    return d

P("apply-new-prices", "Apply the New Prices", "changing-data", "update-rows", "medium",
  """
  `price_changes` lists new prices for some products. Copy each new price into `products`. Products that aren't in
  `price_changes` keep their price.

  Write one `UPDATE` on `products`.
  """,
  [PRODUCTS, PRICE_CHANGES],
  """
  UPDATE products
  SET price = (SELECT c.new_price FROM price_changes c WHERE c.product_id = products.id)
  WHERE id IN (SELECT product_id FROM price_changes)
  """,
  [({"products": SHOP_EX["products"], "price_changes": [(2, 13.5), (4, 7.25)]},
    "The Novel and the Comic get their new prices; the Kettle and the Kite aren't in the list and stay as they were.")],
  reprice_gen,
  wrong=["UPDATE products SET price = (SELECT c.new_price FROM price_changes c WHERE c.product_id = products.id)",
         "UPDATE products SET price = (SELECT MAX(new_price) FROM price_changes) WHERE id IN (SELECT product_id FROM price_changes)"],
  change="products",
  notes="A subquery that finds no row gives NULL, so updating every product would wipe out the prices that have no change. SQLite also accepts `UPDATE products SET price = c.new_price FROM price_changes c WHERE c.product_id = products.id`.")

ACCOUNTS = T("accounts", ("id", "INTEGER", "pk"), ("email", "TEXT"))


def dup_gen(rng, n, k):
    pool = [f"{f.lower()}@mail.test" for f in FIRST[: max(2, n // 2 + 1)]]
    ids = rng.sample(range(1, 4 * n + 10), n + 2)
    return {"accounts": [(i, rng.choice(pool)) for i in ids]}

P("delete-duplicate-emails", "Delete Duplicate Emails", "changing-data", "delete-rows", "medium",
  """
  Some emails are on more than one account. Keep only the account with the **smallest `id`** for each email and delete
  the others.

  Write one `DELETE` on `accounts`.
  """,
  [ACCOUNTS],
  "DELETE FROM accounts WHERE id NOT IN (SELECT MIN(id) FROM accounts GROUP BY email)",
  [({"accounts": [(1, "nia@mail.test"), (2, "omar@mail.test"), (3, "nia@mail.test"), (4, "nia@mail.test")]},
    "Nia's email is on accounts 1, 3 and 4: keep 1, delete 3 and 4. Omar's account stays.")],
  dup_gen,
  wrong=["DELETE FROM accounts WHERE id NOT IN (SELECT MAX(id) FROM accounts GROUP BY email)",
         "DELETE FROM accounts WHERE email IN (SELECT email FROM accounts GROUP BY email HAVING COUNT(*) > 1)"],
  change="accounts")

P("purge-old-cancellations", "Purge Old Cancellations", "changing-data", "delete-rows", "easy",
  """
  Delete every order that was **cancelled** and placed **before 2024-03-01**. Every other order stays.

  Write one `DELETE` on `orders`.
  """,
  [ORDERS],
  "DELETE FROM orders WHERE status = 'cancelled' AND ordered_on < '2024-03-01'",
  [(ex(SHOP_EX, "orders"), "Only order 2 was cancelled, and it was placed in January, so it goes.")],
  lambda rng, n, k: only(shop(rng, n * 2, k, start=(2024, 1, 15), span=90), "orders"),
  wrong=["DELETE FROM orders WHERE status = 'cancelled' OR ordered_on < '2024-03-01'",
         "DELETE FROM orders WHERE status = 'cancelled'"],
  change="orders")


def orphan_gen(rng, n, k):
    d = only(shop(rng, n + 2, k), "orders", "order_items")
    gone = set(rng.sample([o[0] for o in d["orders"]], max(1, len(d["orders"]) // 3)))
    d["orders"] = [o for o in d["orders"] if o[0] not in gone]
    return d

P("remove-orphan-items", "Remove Orphan Items", "changing-data", "delete-rows", "medium",
  """
  Some orders were deleted, but their lines are still in `order_items`. Delete every order line whose `order_id` no
  longer exists in `orders`.

  Write one `DELETE` on `order_items`.
  """,
  [ORDERS, ORDER_ITEMS],
  "DELETE FROM order_items WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.id = order_items.order_id)",
  [({"orders": [o for o in SHOP_EX["orders"] if o[0] != 2], "order_items": SHOP_EX["order_items"]},
    "Order 2 is gone, so its line (three Kites) is deleted. Every other line belongs to an order that still exists.")],
  orphan_gen,
  wrong=["DELETE FROM order_items WHERE order_id IN (SELECT id FROM orders WHERE status = 'cancelled')",
         "DELETE FROM order_items WHERE product_id NOT IN (SELECT id FROM orders)"],
  change="order_items")

ARCHIVE = T("orders_archive", ("id", "INTEGER", "pk"), ("customer_id", "INTEGER"), ("ordered_on", "TEXT"), ("status", "TEXT"))


def archive_gen(rng, n, k):
    d = only(shop(rng, n * 2, k, start=(2023, 11, 1), span=120), "orders")
    old = [o for o in d["orders"] if o[2] < "2024-01-01"]
    d["orders_archive"] = rng.sample(old, len(old) // 2) if old else []
    return d

P("archive-last-year", "Archive Last Year", "changing-data", "insert-upsert", "medium",
  """
  Copy every order placed **before 2024-01-01** into `orders_archive`, with all four columns. Some of those orders were
  already archived; don't copy them again (`orders_archive.id` must stay unique). `orders` itself doesn't change.

  Write one `INSERT` into `orders_archive`.
  """,
  [ORDERS, ARCHIVE],
  """
  INSERT INTO orders_archive (id, customer_id, ordered_on, status)
  SELECT id, customer_id, ordered_on, status
  FROM orders
  WHERE ordered_on < '2024-01-01'
    AND id NOT IN (SELECT id FROM orders_archive)
  """,
  [({"orders": [(1, 1, "2023-12-20", "delivered"), (2, 2, "2023-12-31", "cancelled"), (3, 1, "2024-01-01", "delivered")],
     "orders_archive": [(1, 1, "2023-12-20", "delivered")]},
    "Order 2 is from 2023 and not archived yet, so it's copied. Order 1 is already there, and order 3 is from 2024.")],
  archive_gen,
  wrong=["INSERT INTO orders_archive (id, customer_id, ordered_on, status) SELECT id, customer_id, ordered_on, status FROM orders WHERE ordered_on < '2024-01-01'",
         "INSERT INTO orders_archive (id, customer_id, ordered_on, status) SELECT id, customer_id, ordered_on, status FROM orders WHERE ordered_on <= '2024-01-01' AND id NOT IN (SELECT id FROM orders_archive)"],
  change="orders_archive")

INVENTORY = T("inventory", ("sku", "TEXT", "pk"), ("qty", "INTEGER"))
DELIVERIES = T("deliveries", ("sku", "TEXT", "pk"), ("qty", "INTEGER"))


def stock_gen(rng, n, k):
    skus = [f"SKU-{i:03d}" for i in rng.sample(range(1, 400), n + 4)]
    have = rng.sample(skus, max(1, len(skus) // 2))
    came = rng.sample(skus, max(1, len(skus) // 2))
    return {"inventory": [(s, rng.randint(0, 40)) for s in have], "deliveries": [(s, rng.randint(1, 30)) for s in came]}

P("restock-inventory", "Restock the Inventory", "changing-data", "insert-upsert", "medium",
  """
  Today's `deliveries` (one row per `sku`) have arrived. Add each delivered quantity to that SKU's `qty` in `inventory`;
  a SKU that isn't in `inventory` yet is added with the delivered quantity.

  Write one `INSERT` into `inventory` that also updates existing SKUs.
  """,
  [INVENTORY, DELIVERIES],
  """
  INSERT INTO inventory (sku, qty)
  SELECT sku, qty FROM deliveries WHERE true
  ON CONFLICT (sku) DO UPDATE SET qty = inventory.qty + excluded.qty
  """,
  [({"inventory": [("SKU-001", 10), ("SKU-002", 0)], "deliveries": [("SKU-002", 5), ("SKU-003", 8)]},
    "SKU-002 goes from 0 to 5, SKU-003 is new with 8, and SKU-001 got nothing today.")],
  stock_gen,
  wrong=["INSERT INTO inventory (sku, qty) SELECT sku, qty FROM deliveries WHERE true ON CONFLICT (sku) DO UPDATE SET qty = excluded.qty",
         "INSERT OR IGNORE INTO inventory (sku, qty) SELECT sku, qty FROM deliveries"],
  change="inventory",
  notes="`excluded.qty` is the value the `INSERT` tried to add. With `INSERT … SELECT … ON CONFLICT`, SQLite needs a `WHERE` clause (even `WHERE true`) so it can tell where the `SELECT` ends.")

done()
