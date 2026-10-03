"""Builds solution.json: the written-out solution behind the problem page's
Solution tab. One sol() call per problem, grouped by topic (arrays.py, ...).
Run a topic file to (re)write its problems' solution.json files, then check the
code with `npm run check:solutions`.

Text uses the statements' small Markdown: paragraphs, "- " and "1. " lists,
**bold** and `code`. A section is a list of blocks: a string is text,
fig(...) is a row of drawings, and table(...) is a small table.

Code comes in all four languages. Lines are tagged for the line-by-line
breakdown with a marker comment at the end of the line, `#@2` in Python and
`//@2` elsewhere; the markers are stripped and become line ranges per language.
A tag that only one language has (C's hand-written hash table, say) makes a
breakdown row that only that language shows.
"""
import json
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "visuals"))
from lib import Grid, L, NT, Row, Vars, find, fmt  # noqa: E402,F401

LANGS = ["python", "java", "cpp", "c"]
KINDS = {"brute": "Brute force", "better": "Better", "best": "Best"}
MARK = re.compile(r"\s*(?:#|//)@(\w+)\s*$")
WRITTEN = []
REGISTRY = []


def problem(fn):
    """Register a function that writes one problem's solution; its name is the id with _ for -."""
    REGISTRY.append(fn)
    return fn


def run(only=()):
    for fn in REGISTRY:
        pid = fn.__name__.replace("_", "-")
        if not only or pid in only:
            fn()
    print(f"wrote {len(WRITTEN)} solutions: {', '.join(WRITTEN)}")


def dd(s):
    return textwrap.dedent(s).strip("\n")


def fig(*panels, caption=None):
    b = {"panels": [p for p in panels if p]}
    if caption:
        b["caption"] = caption
    return b


def table(head, *rows):
    return {"table": {"head": [str(h) for h in head], "rows": [[str(c) for c in r] for r in rows]}}


def blocks(items, where):
    out = []
    for b in items:
        if isinstance(b, str):
            out.append({"md": dd(b)})
        elif isinstance(b, dict) and ("panels" in b or "table" in b):
            out.append(b)
        elif isinstance(b, dict) and "type" in b:
            out.append({"panels": [b]})
        else:
            raise ValueError(f"{where}: can't use block {b!r}")
    return out


class Steps:
    """A step-by-step player (the problem page's walkthrough), recorded by running the idea."""

    def __init__(self, title=None):
        self.title, self.steps = title, []

    def step(self, text, *panels, result=None):
        s = {"text": text, "panels": [p for p in panels if p]}
        if result is not None:
            s["result"] = fmt(result)
        self.steps.append(s)

    def spec(self):
        assert 2 <= len(self.steps) <= 40, f"a walkthrough needs 2-40 steps, has {len(self.steps)}"
        out = {"steps": self.steps}
        if self.title:
            out["title"] = self.title
        return out


def ranges(nums):
    out = []
    for n in sorted(set(nums)):
        if out and n == out[-1][1] + 1:
            out[-1][1] = n
        else:
            out.append([n, n])
    return out


def parse(src):
    """Code with marker comments -> (clean code, {tag: [line numbers]})."""
    lines, tags = [], {}
    for i, line in enumerate(dd(src).split("\n"), 1):
        m = MARK.search(line)
        if m:
            tags.setdefault(m.group(1), []).append(i)
            line = line[: m.start()]
        lines.append(line.rstrip())
    # Pieces joined from differently indented strings dedent badly: the top-level
    # lines would then sit far to the right. Catch that here.
    starts = [l for l in lines if l.strip()][:1]
    assert starts and not starts[0].startswith(" "), "code starts indented"
    ind = [len(l) - len(l.lstrip(" ")) for l in lines if l.strip()]
    jumps = [b - a for a, b in zip(ind, ind[1:])]
    assert max(jumps, default=0) <= 12, "code indentation jumps too far (pieces joined with mixed indentation?)"
    return "\n".join(lines) + "\n", tags


def approach(title, kind, time, space, idea, build, code, lines, complexity, walk=None, limits=None, slow=False, langs=None):
    """One way to solve it. kind: brute, better or best.
    slow: too slow for the big tests, so the checker runs it on small ones only
    (True: inputs up to 2500 characters; a number: up to that many)."""
    assert kind in KINDS, kind
    langs = langs or LANGS  # design problems (classes) have no C version
    assert set(code) == set(langs), f"{title}: code needs {langs}, has {sorted(code)}"
    clean, tags = {}, {}
    for lang in langs:
        clean[lang], tags[lang] = parse(code[lang])
    used = {t for lang in langs for t in tags[lang]}
    rows = []
    for entry in lines:
        tag, text = str(entry[0]), entry[1]
        notes = entry[2] if len(entry) > 2 else {}
        at = {lang: ranges(tags[lang][tag]) for lang in langs if tag in tags[lang]}
        assert at, f"{title}: breakdown row @{tag} matches no code line"
        assert set(notes) <= set(at), f"{title}: @{tag} has a note for a language without that line"
        row = {"text": dd(text), "at": at, "tag": tag}
        if notes:
            row["notes"] = {k: dd(v) for k, v in notes.items()}
        rows.append(row)
    missing = used - {str(e[0]) for e in lines}
    assert not missing, f"{title}: code tags {sorted(missing)} have no breakdown row"
    a = {
        "title": title,
        "kind": kind,
        "time": time,
        "space": space,
        "idea": blocks(idea, title),
        "build": [dd(s) for s in build],
        "code": clean,
        "lines": rows,
        "complexity": blocks(complexity, title),
    }
    if walk is not None:
        a["walk"] = walk.spec() if isinstance(walk, Steps) else walk
    if limits:
        a["limits"] = blocks(limits, title)
    if slow:
        a["slow"] = slow if isinstance(slow, int) and not isinstance(slow, bool) else True
    return a


EXTRA = {}  # pid -> fuller text that replaces sections of that problem's sol() call


def sol(pid, summary, question, think, approaches, takeaways):
    """Write problems/.../<pid>/solution.json."""
    x = EXTRA.get(pid, {})
    question = list(question) + list(x.get("question_more", []))
    think = x.get("think", think)
    takeaways = x.get("takeaways", takeaways)
    for i, more in x.get("approaches", {}).items():
        a = approaches[i]
        for key in ("idea", "complexity", "limits"):
            if key in more:
                a[key] = blocks(more[key], a["title"])
        if "build" in more:
            a["build"] = [dd(b) for b in more["build"]]
        if "lines" in more:
            known = {row["tag"] for row in a["lines"]}
            assert set(more["lines"]) <= known, f"{pid} #{i}: unknown line tags {set(more['lines']) - known}"
            for row in a["lines"]:
                if row["tag"] in more["lines"]:
                    row["text"] = dd(more["lines"][row["tag"]])
    for a in approaches:
        for row in a["lines"]:
            row.pop("tag", None)
    assert approaches, pid
    assert approaches[-1]["kind"] == "best", f"{pid}: the last approach should be the best one"
    for a in approaches[:-1]:
        assert a.get("limits"), f"{pid}: '{a['title']}' needs 'limits' (where it falls short)"
    data = {
        "version": 1,
        "summary": dd(summary),
        "question": blocks(question, "question"),
        "think": blocks(think, "think"),
        "approaches": approaches,
        "takeaways": blocks(takeaways, "takeaways"),
    }
    path = os.path.join(find(pid), "solution.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
        f.write("\n")
    WRITTEN.append(pid)
    return data
