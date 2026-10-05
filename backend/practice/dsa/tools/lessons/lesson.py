"""Builds a pattern lesson: the long-form explanation a learner reads on
learn.html before solving that pattern's problems. One module per pattern
(arrays_lessons/<pattern>.py) calls lesson(); build.py writes the JSON to
backend/practice/dsa/lessons/<topic>/<pattern>.json and checks every code block.

A section is a list of blocks, as in solutions (sol.py): a string is text in the
statements' small Markdown, fig(...) is a row of drawings, table(...) a table.
Lessons add:
  key(md)          the one idea to remember, set apart from the text
  walk(Steps)      a step-by-step player recorded by running the idea
  code(...)        code in Python, Java, C++ and C with a line-by-line
                   breakdown and an example run. A hidden `run` harness per
                   language calls the code; build.py compiles and runs all four
                   and requires each to print exactly `output`.
  quiz((q, a), …)  questions to check yourself, answers hidden until asked

Code lines are tagged for the breakdown like solutions: `#@tag` in Python,
`//@tag` elsewhere. Java code is a set of static methods (the harness puts them
in a class); C++ and C code is top-level functions.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "solutions"))
from sol import Steps, dd, fig, parse, ranges, table  # noqa: E402,F401
from lib import Grid, Row, Vars, fmt  # noqa: E402,F401  (tools/visuals, put on the path by sol)
import leetcode  # noqa: E402

DSA = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(DSA, "lessons")
LANGS = ["python", "java", "cpp", "c"]
WRITTEN = []
CHECKS = []  # (lesson id, block title, {lang: harness}, expected output, {lang: shown code})


def M(items, label=None):
    """A key -> value panel (a map, a few variables), keys in the given order."""
    p = {"type": "vars", "items": {f"{k}:": fmt(v) for k, v in dict(items).items()}}
    if label:
        p["label"] = label
    return p


def Bars(values, labels=None, st=None, ptr=None, label=None, height=None, top=None, bottom=None):
    """Values as bars on a zero line; labels default to the indices. top / bottom fix the scale (for walkthroughs)."""
    p = {"type": "bars", "values": list(values)}
    if labels is not None:
        p["labels"] = [str(x) for x in labels]
    if st:
        p["states"] = {str(k): v for k, v in st.items() if v}
    if ptr:
        p["pointers"] = {k: v for k, v in ptr.items() if v is not None}
    if label:
        p["label"] = label
    if height:
        p["height"] = height
    if top is not None:
        p["max"] = top
    if bottom is not None:
        p["min"] = bottom
    return p


def key(md):
    return {"key": dd(md)}


def walk(steps, intro=None, legend=None):
    """legend: {state: what that colour means here}, shown under the player."""
    b = {"walk": steps.spec()}
    if intro:
        b["intro"] = dd(intro)
    if legend:
        b["walk"]["legend"] = [{"state": k, "text": dd(v)} for k, v in legend.items()]
    return b


# Topics written before walkthroughs had to keep one layout and explain their colours.
# Their walkthroughs still change panels between steps; new topics must not.
LAYOUT_EXEMPT = {"arrays-hashing"}
SAME_LOOK = {"found", "new"}  # drawn identically, so one walkthrough may use only one of them


def check_walk(where, w):
    """Every step shows the same panels (types and labels) in the same order, and every colour used is in the legend."""
    looks = [tuple((p["type"], p.get("label")) for p in s["panels"]) for s in w["steps"]]
    assert len(set(looks)) == 1, f"{where}: walkthrough panels change between steps: {sorted(set(looks), key=str)}"
    used = {v for s in w["steps"] for p in s["panels"] for v in (p.get("states") or {}).values()}
    keyed = {x["state"] for x in w.get("legend", [])}
    assert used <= keyed, f"{where}: colours {sorted(used - keyed)} are used but not in the legend"
    assert not (keyed - used), f"{where}: legend lists colours {sorted(keyed - used)} that no step uses"
    assert not SAME_LOOK <= used, f"{where}: 'found' and 'new' look the same; use one of them"


def quiz(*pairs):
    assert pairs and all(len(p) == 2 for p in pairs)
    return {"quiz": [{"q": dd(q), "a": dd(a)} for q, a in pairs]}


def code(title, code, lines, run, call, output=None):
    """One piece of code in every language.
    lines: [(tag, text)] or [(tag, text, {lang: note})], like solutions.
    run: {lang: harness source} that calls the code and prints.
    call: what the harness runs, shown under the code (e.g. "count([3, 1, 3])").
    output: what every language must print; by default, what the Python code prints."""
    assert set(code) == set(LANGS), f"{title}: code needs {LANGS}, has {sorted(code)}"
    assert set(run) == set(LANGS), f"{title}: run needs {LANGS}, has {sorted(run)}"
    clean, tags = {}, {}
    for lang in LANGS:
        clean[lang], tags[lang] = parse(code[lang])
    used = {t for lang in LANGS for t in tags[lang]}
    rows = []
    for entry in lines:
        tag, text = str(entry[0]), entry[1]
        notes = entry[2] if len(entry) > 2 else {}
        at = {lang: ranges(tags[lang][tag]) for lang in LANGS if tag in tags[lang]}
        assert at, f"{title}: breakdown row @{tag} matches no code line"
        assert set(notes) <= set(at), f"{title}: @{tag} has a note for a language without that line"
        row = {"text": dd(text), "at": at}
        if notes:
            row["notes"] = {k: dd(v) for k, v in notes.items()}
        rows.append(row)
    missing = used - {str(e[0]) for e in lines}
    assert not missing, f"{title}: code tags {sorted(missing)} have no breakdown row"
    if output is None:
        output = pyrun(clean["python"], dd(run["python"]))
    output = output if output.endswith("\n") else output + "\n"
    return {
        "code": clean,
        "title": title,
        "lines": rows,
        "run": {"call": call, "output": output.rstrip("\n")},
        "_check": {lang: dd(run[lang]) for lang in LANGS},
        "_output": output,
    }


def pyrun(src, harness):
    """Run Python code plus its harness here and return what it prints."""
    import contextlib
    import io

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(src + "\n" + harness + "\n", "<lesson>", "exec"), {"__name__": "__lesson__"})
    return buf.getvalue()


def py(src, name):
    """Run tagged Python lesson code and hand back one of its functions."""
    ns = {}
    exec(parse(src)[0], ns)
    return ns[name]


def blocks(items, where):
    out = []
    for b in items:
        if isinstance(b, str):
            out.append({"md": dd(b)})
        elif isinstance(b, dict) and ({"panels", "table", "key", "walk", "quiz", "code"} & set(b)):
            out.append(b)
        elif isinstance(b, dict) and "type" in b:
            out.append({"panels": [b]})
        else:
            raise ValueError(f"{where}: can't use block {b!r}")
    return out


def _words(blocks_):
    n = 0
    for b in blocks_:
        for k in ("md", "key"):
            if k in b:
                n += len(b[k].split())
        if "quiz" in b:
            n += sum(len(x["q"].split()) + len(x["a"].split()) for x in b["quiz"])
        if "code" in b:
            n += 40 + sum(len(r["text"].split()) for r in b["lines"])
        if "walk" in b:
            n += sum(len(s["text"].split()) + 6 for s in b["walk"]["steps"])
        if "table" in b:
            n += 4 * len(b["table"]["rows"])
    return n


def lesson(topic, pattern, summary, sections):
    """Write lessons/<topic>/<pattern>.json. sections: [(id, title, [blocks])]."""
    ids = [s[0] for s in sections]
    assert len(set(ids)) == len(ids), f"{pattern}: duplicate section ids"
    out = []
    for sid, title, items in sections:
        assert re.fullmatch(r"[a-z][a-z0-9-]*", sid), sid
        out.append({"id": sid, "title": title, "blocks": blocks(items, f"{pattern}/{sid}")})
    for s in out:
        for b in s["blocks"]:
            if "code" in b:
                CHECKS.append((pattern, b["title"], b.pop("_check"), b.pop("_output"), b["code"]))
    if topic not in LAYOUT_EXEMPT:
        for s in out:
            for b in s["blocks"]:
                if "walk" in b:
                    check_walk(f"{pattern}/{s['id']}", b["walk"])
    words = sum(_words(s["blocks"]) for s in out)
    data = {
        "version": 1,
        "id": pattern,
        "topic": topic,
        "summary": dd(summary),
        "minutes": max(5, round(words / 200)),
        "sections": out,
        "leetcode": leetcode.entries(pattern),
    }
    os.makedirs(os.path.join(OUT, topic), exist_ok=True)
    with open(os.path.join(OUT, topic, f"{pattern}.json"), "w") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
        f.write("\n")
    WRITTEN.append(pattern)
    return data
