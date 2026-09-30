"""Write a problem folder from one compact call. Used when authoring problems in bulk.

    import sys; sys.path.insert(0, "backend/practice/dsa/tools")
    from author import P, ex, sample, edge, gen

    P("binary-search/classic-search/find-the-shelf",
      title="Find the Shelf", difficulty="easy",
      sig="findShelf(shelves: int[], target: int) -> int",
      hint="...", nudge="...", tags=["arrays"],
      statement=r'''...{{examples}}...''',
      reference=r'''...''', brute=r'''...''', validator=r'''...''', gen=r'''...''',
      wrong={"off_by_one": r'''...'''},
      tests=[ex({...}, 3, "why"), sample({...}), edge("single", {...}), gen("random", "--n 50", 10)])

Design problems use sig="class Name(cap: int); get(key: int) -> int; put(key: int, value: int) -> void".
The pipeline (check.mjs --write-expected) fills in every expected answer that isn't given.
"""
import json
import os
import re
import textwrap
import zlib

DSA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROBLEMS = os.path.join(DSA, "problems")


def _params(text):
    text = text.strip()
    if not text:
        return []
    out = []
    for part in text.split(","):
        name, type_ = [x.strip() for x in part.split(":")]
        out.append({"name": name, "type": type_})
    return out


def _signature(sig):
    sig = sig.strip()
    if sig.startswith("class "):
        parts = [p.strip() for p in sig[len("class "):].split(";") if p.strip()]
        m = re.fullmatch(r"(\w+)\((.*)\)", parts[0])
        design = {"class": m.group(1), "constructor": {"params": _params(m.group(2))}, "methods": []}
        for p in parts[1:]:
            m = re.fullmatch(r"(\w+)\((.*)\)\s*->\s*(\S+)", p)
            design["methods"].append({"name": m.group(1), "params": _params(m.group(2)), "returns": m.group(3)})
        return "design", design
    m = re.fullmatch(r"(\w+)\((.*)\)\s*->\s*(\S+)", sig)
    return "function", {"function": m.group(1), "params": _params(m.group(2)), "returns": m.group(3)}


def _yaml_value(v):
    return json.dumps(v, ensure_ascii=False)


def _yaml_params(params):
    return "[" + ", ".join("{ name: %s, type: %s }" % (p["name"], _yaml_value(p["type"])) for p in params) + "]"


def ex(input, expected, explanation):
    return {"visible": True, "example": True, "kind": "example", "input": input, "expected": expected, "explanation": explanation}


def sample(input, expected=None):
    t = {"visible": True, "kind": "sample", "input": input}
    if expected is not None:
        t["expected"] = expected
    return t


def edge(name, input, no_brute=False):
    t = {"id": "edge-" + name, "visible": False, "kind": "edge", "input": input}
    if no_brute:  # short input but huge values: too slow for brute.py
        t["no_brute"] = True
    return t


def gen(name, args, count=1, kind="random"):
    g = {"args": args}
    if count > 1:
        g["count"] = count
    return {"id": name, "visible": False, "kind": kind, "generate": g}


def maxgen(name, args, count=1):
    return gen(name, args, count, kind="max")


def _clean(code):
    return textwrap.dedent(code).strip("\n") + "\n"


def P(path, title, difficulty, sig, hint, nudge, statement, reference, brute, validator, gen, wrong,
      tests, tags=(), time_ms=1000, memory_mb=256, checker="exact", tolerance=None, checker_py=None, seed=None):
    topic, pattern, pid = path.split("/")
    d = os.path.join(PROBLEMS, topic, pattern, pid)
    os.makedirs(os.path.join(d, "wrong"), exist_ok=True)
    kind, spec = _signature(sig)

    lines = [
        "schema_version: 1",
        "id: " + pid,
        "title: " + _yaml_value(title),
        "topic: " + topic,
        "pattern: " + pattern,
        "tags: [" + ", ".join(tags) + "]",
        "difficulty: " + difficulty,
        "status: draft",
        "version: 1",
        "kind: " + kind,
    ]
    if kind == "function":
        lines.append("signature: { function: %s, params: %s, returns: %s }" % (spec["function"], _yaml_params(spec["params"]), _yaml_value(spec["returns"])))
    else:
        lines += [
            "design:",
            "  class: " + spec["class"],
            "  constructor: { params: %s }" % _yaml_params(spec["constructor"]["params"]),
            "  methods:",
        ] + ["    - { name: %s, params: %s, returns: %s }" % (m["name"], _yaml_params(m["params"]), _yaml_value(m["returns"])) for m in spec["methods"]]
    lines.append("limits: { time_ms: %d, memory_mb: %d }" % (time_ms, memory_mb))
    lines.append("checker: { type: %s%s }" % (checker, ", tolerance: %s" % tolerance if tolerance else ""))
    lines += ["hints:", "  hint: " + _yaml_value(hint.strip()), "  nudge: " + _yaml_value(nudge.strip()), "authors: [ren]", "reviewed_by: []"]

    files = {
        "problem.yaml": "\n".join(lines) + "\n",
        "statement.md": _clean(statement),
        "reference.py": _clean(reference),
        "brute.py": _clean(brute),
        "validator.py": _clean(validator),
        "gen.py": _clean(gen),
    }
    if checker_py:
        files["checker.py"] = _clean(checker_py)
    for name, code in wrong.items():
        files[os.path.join("wrong", name if name.endswith(".py") else name + ".py")] = _clean(code)

    n_ex = n_sample = 0
    out_tests = []
    for t in tests:
        t = dict(t)
        if "id" not in t:
            if t["kind"] == "example":
                n_ex += 1
                t["id"] = "ex%d" % n_ex
            else:
                n_sample += 1
                t["id"] = "sample%d" % n_sample
        out_tests.append({"id": t.pop("id"), **t})
    doc = {"problem": pid, "version": 1, "seed": seed if seed is not None else zlib.crc32(pid.encode()) % 10**8, "tests": out_tests}
    files["tests.json"] = _format_tests(doc)

    for name, content in files.items():
        with open(os.path.join(d, name), "w") as f:
            f.write(content)
    return d


def _format_tests(doc):
    inline = lambda v: json.dumps(v, separators=(",", ":"), ensure_ascii=False)
    head = ",\n".join("  %s: %s" % (json.dumps(k), inline(v)) for k, v in doc.items() if k != "tests")
    body = ",\n".join("    {\n" + ",\n".join("      %s: %s" % (json.dumps(k), inline(v)) for k, v in t.items()) + "\n    }" for t in doc["tests"])
    return "{\n" + head + ',\n  "tests": [\n' + body + "\n  ]\n}\n"
