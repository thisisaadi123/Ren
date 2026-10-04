"""Write the pattern lessons and check their code.

    npm run lessons                       every lesson
    npm run lessons -- prefix-sums        just these patterns
    npm run lessons -- --no-check         write the JSON without running code

Every code block is compiled and run in Python, Java, C++ and C with its hidden
harness; each language must print exactly the output the lesson shows.
"""
import importlib
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

import lesson

TOPICS = {"arrays-hashing": "arrays_lessons"}
BUILD = os.path.join(lesson.DSA, "build", "lessons")
JAVA_BINS = [os.environ.get("JAVA_HOME") and os.path.join(os.environ["JAVA_HOME"], "bin"), "/opt/homebrew/opt/openjdk@21/bin", "/opt/homebrew/opt/openjdk/bin"]
JAVA = next((d for d in JAVA_BINS if d and os.path.exists(os.path.join(d, "javac"))), "")

CPP_PRE = """#include <algorithm>
#include <array>
#include <climits>
#include <iostream>
#include <map>
#include <numeric>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
using namespace std;
"""
C_PRE = """#include <limits.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
"""


def program(lang, src, run):
    if lang == "python":
        return src + "\n\n" + run + "\n"
    if lang == "java":
        return "import java.util.*;\n\npublic class Main {\n" + src + "\n" + run + "\n}\n"
    if lang == "cpp":
        return CPP_PRE + "\n" + src + "\n" + run + "\n"
    return C_PRE + "\n" + src + "\n" + run + "\n"


def sh(cmd, cwd, stdin=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=120, input=stdin)
    return r.returncode, r.stdout, r.stderr


def check_one(job):
    n, (pattern, title, run, output, code) = job
    problems = []
    for lang in lesson.LANGS:
        d = os.path.join(BUILD, pattern, f"{n}-{lang}")
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
        src = program(lang, code[lang], run[lang])
        if lang == "python":
            open(os.path.join(d, "main.py"), "w").write(src)
            rc, out, err = sh([sys.executable, "main.py"], d)
        elif lang == "java":
            open(os.path.join(d, "Main.java"), "w").write(src)
            rc, out, err = sh([os.path.join(JAVA, "javac"), "-Xlint:none", "Main.java"], d)
            if rc == 0:
                rc, out, err = sh([os.path.join(JAVA, "java"), "-cp", ".", "Main"], d)
        elif lang == "cpp":
            open(os.path.join(d, "main.cpp"), "w").write(src)
            rc, out, err = sh(["clang++", "-std=c++17", "-O2", "-Wall", "-Werror", "-Wno-unused-function", "-o", "main", "main.cpp"], d)
            if rc == 0:
                rc, out, err = sh(["./main"], d)
        else:
            open(os.path.join(d, "main.c"), "w").write(src)
            rc, out, err = sh(["clang", "-std=c11", "-O2", "-Wall", "-Werror", "-Wno-unused-function", "-o", "main", "main.c", "-lm"], d)
            if rc == 0:
                rc, out, err = sh(["./main"], d)
        if rc != 0:
            problems.append(f"{pattern} · {title} · {lang}: failed\n{err.strip()[:1500]}")
        elif out != output:
            problems.append(f"{pattern} · {title} · {lang}: printed\n{out}expected\n{output}")
    return problems


def main(argv):
    only = [a for a in argv if not a.startswith("--")]
    for topic, package in TOPICS.items():
        pkg = importlib.import_module(package)
        for name in pkg.ORDER:
            pid = name.replace("_", "-")
            if not only or pid in only:
                importlib.import_module(f"{package}.{name}")
    print(f"wrote {len(lesson.WRITTEN)} lessons: {', '.join(lesson.WRITTEN)}")
    if "--no-check" in argv:
        return 0
    jobs = list(enumerate(lesson.CHECKS))
    with ThreadPoolExecutor(max_workers=4) as pool:
        problems = [p for ps in pool.map(check_one, jobs) for p in ps]
    print(f"checked {len(jobs)} code blocks in {len(lesson.LANGS)} languages")
    for p in problems:
        print("\n" + p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
