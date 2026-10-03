"""Writes SQL problems for the bank: one P(...) call per problem.

P() writes problems/<topic>/<pattern>/<id>/problem.json (statement, tables,
reference and wrong queries) and tests.json (example and hidden datasets).
Expected answers are filled in by running the reference:
    node backend/practice/sql/tools/check.mjs --write-expected <dir>

A table is T("name", ("col", "TYPE"), ("id", "INTEGER", "pk"), ("x_id", "INTEGER", "fk other.id")).
A dataset is {"table": [(row), ...]} with values in column order.
gen(rng, n, k) builds hidden dataset k at scale n (roughly the main table's size).
"""
import json
import os
import random
import textwrap
import zlib

SQL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROBLEMS = os.path.join(SQL, "problems")
WRITTEN = []

# Hidden datasets per difficulty, by scale. Small ones catch edge cases, big ones catch luck.
SIZES = {
    "easy": [1, 2, 3, 5, 8, 12, 20, 35, 60, 120],
    "medium": [1, 2, 3, 4, 6, 9, 14, 20, 30, 50, 90, 200],
    "hard": [1, 2, 3, 4, 5, 7, 10, 14, 20, 30, 45, 70, 120, 250],
}

FIRST = """Ava Bilal Chen Dara Elif Farah Gus Hana Ivo Jae Kofi Lena Mateo Nia Omar Priya Quinn Rosa Sami Tara
Uma Vik Wen Xavi Yara Zane Abel Bea Cyrus Dina Emil Fern Gale Hugo Ines Juno Kai Lior Mina Noor Otto Pia Rafa
Suki Teo Ulla Vera Wade Yusuf Zara Arlo Cleo Dev Esme Finn Gia Hiro Isla Joel Kira Luca Maya Nils Opal Pax Remy
Sana Theo Una Vito Willa Yael Zeke Asha Bram Coco Dani Ezra""".split()
LAST = """Ade Brook Cruz Diaz Ebert Fox Gray Holt Ito Jain Kerr Lund Moss Nair Oduya Park Quist Reyes Sato Tran
Ueda Vance Wolfe Xu Young Zito Amar Bose Cole Dunn""".split()
CITIES = ["Lisbon", "Osaka", "Nairobi", "Denver", "Pune", "Quito", "Oslo", "Austin", "Hanoi", "Leeds"]


def T(name, *cols):
    return {"name": name, "columns": [list(c) for c in cols]}


def dd(s):
    return textwrap.dedent(s).strip("\n")


def names(rng, n):
    """n distinct person names."""
    pool = [f"{f} {l}" for f in FIRST for l in LAST]
    return rng.sample(pool, n)


def firsts(rng, n):
    """n distinct first names (n <= len(FIRST)), else distinct full names."""
    return rng.sample(FIRST, n) if n <= len(FIRST) else names(rng, n)


def day(offset, base=(2024, 1, 1)):
    import datetime
    return (datetime.date(*base) + datetime.timedelta(days=offset)).isoformat()


def maybe(rng, p, v):
    return None if rng.random() < p else v


def _check(tables, data, where):
    cols = {t["name"]: t["columns"] for t in tables}
    for tname, rows in data.items():
        assert tname in cols, f"{where}: unknown table {tname}"
        width = len(cols[tname])
        pks = [i for i, c in enumerate(cols[tname]) if len(c) > 2 and c[2] == "pk"]
        seen = set()
        for r in rows:
            assert len(r) == width, f"{where}: {tname} row {r} needs {width} values"
            for i in pks:
                assert r[i] not in seen, f"{where}: {tname} repeats key {r[i]}"
                seen.add(r[i])
    for t in tables:
        data.setdefault(t["name"], [])
    return {k: [list(r) for r in v] for k, v in data.items()}


def P(id, title, topic, pattern, difficulty, statement, tables, reference, examples, gen,
      ordered=False, wrong=(), notes="", sizes=None, change=None):
    """change="table" makes it a change problem: the answer is one UPDATE/DELETE/INSERT,
    judged on that table's rows afterwards (in any order)."""
    assert difficulty in SIZES
    rng = random.Random(zlib.crc32(id.encode()))
    tests = []
    for i, ex in enumerate(examples):
        data, why = ex if isinstance(ex, tuple) else (ex, "")
        t = {"id": f"ex{i + 1}", "example": True, "data": _check(tables, dict(data), f"{id} ex{i + 1}")}
        if why:
            t["explanation"] = dd(why)
        tests.append(t)
    for k, n in enumerate(sizes or SIZES[difficulty]):
        data = _check(tables, gen(rng, n, k), f"{id} hidden {k + 1}")
        tests.append({"id": f"h{k + 1}", "example": False, "data": data})

    dirpath = os.path.join(PROBLEMS, topic, pattern, id)
    os.makedirs(dirpath, exist_ok=True)
    meta = {
        "id": id, "title": title, "topic": topic, "pattern": pattern, "difficulty": difficulty,
        "statement": dd(statement), "notes": dd(notes), "tables": tables, "ordered": ordered,
        "reference": dd(reference), "wrong": [dd(w) for w in wrong],
    }
    if change:
        assert not ordered, "a change problem compares the table's rows in any order"
        meta["mode"] = "change"
        meta["result_table"] = change
    with open(os.path.join(dirpath, "problem.json"), "w") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
        f.write("\n")
    with open(os.path.join(dirpath, "tests.json"), "w") as f:
        f.write('{"problem": %s, "tests": [\n' % json.dumps(id))
        f.write(",\n".join("  " + json.dumps(t, ensure_ascii=False) for t in tests))
        f.write("\n]}\n")
    WRITTEN.append(id)


def done():
    print(f"wrote {len(WRITTEN)} problems: {', '.join(WRITTEN)}")
