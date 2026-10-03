"""Small hand-made datasets shared by several problems' examples."""
EMP_EX = {"employees": [
    (1, "Ava Moss", 1, None, 96000, "2019-03-04"),
    (2, "Bilal Cruz", 2, 1, 61000, "2020-07-15"),
    (3, "Chen Ito", 1, 1, 60000, "2021-01-10"),
    (4, "Dara Kerr", None, 2, 125500, "2019-03-04"),
    (5, "Elif Park", 2, 2, 48000, "2022-11-30"),
]}
STAFF_EX = {"departments": [(1, "Design", "Lisbon"), (2, "Sales", "Osaka"), (3, "Legal", "Denver")], **EMP_EX}
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
LATEST_EX = {"orders": [(1, 1, "2024-01-03", "delivered"), (2, 2, "2024-01-03", "shipped"), (3, 1, "2024-01-05", "delivered"),
                        (4, 3, "2024-01-06", "cancelled"), (5, 2, "2024-01-09", "delivered"), (6, 2, "2024-01-09", "shipped")]}
