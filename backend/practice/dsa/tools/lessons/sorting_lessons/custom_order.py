"""Lesson: Custom order (Sorting, pattern 2)."""
from functools import cmp_to_key

from lesson import M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

RANK = {
    "python": """
        def rank_players(players):
            return sorted(players, key=lambda p: (-p[1], p[0]))    #@key
    """,
    "java": """
        record Player(String name, int score) {}

        static List<Player> rankPlayers(List<Player> players) {
            List<Player> out = new ArrayList<>(players);            //@copy
            out.sort(Comparator.comparingInt((Player p) -> p.score()).reversed()   //@key
                     .thenComparing(Player::name));                 //@key
            return out;                                             //@ret
        }
    """,
    "cpp": """
        struct Player {
            string name;
            int score;
        };

        vector<Player> rankPlayers(vector<Player> players) {
            sort(players.begin(), players.end(), [](const Player& a, const Player& b) {  //@key
                if (a.score != b.score) return a.score > b.score;   //@first
                return a.name < b.name;                             //@second
            });
            return players;                                         //@ret
        }
    """,
    "c": """
        typedef struct {
            const char* name;
            int score;
        } Player;

        static int byRank(const void* x, const void* y) {
            const Player* a = x;                                    //@key
            const Player* b = y;                                    //@key
            if (a->score != b->score) return a->score > b->score ? -1 : 1;  //@first
            return strcmp(a->name, b->name);                        //@second
        }

        void rankPlayers(Player* players, int n) {
            qsort(players, n, sizeof(Player), byRank);              //@ret
        }
    """,
}
RANK_RUN = {
    "python": """
        for name, score in rank_players([("mia", 82), ("ali", 95), ("zoe", 82), ("ben", 70), ("cal", 95)]):
            print(name, score)
    """,
    "java": """
        public static void main(String[] args) {
            List<Player> ps = List.of(new Player("mia", 82), new Player("ali", 95), new Player("zoe", 82), new Player("ben", 70), new Player("cal", 95));
            for (Player p : rankPlayers(ps)) System.out.println(p.name() + " " + p.score());
        }
    """,
    "cpp": """
        int main() {
            vector<Player> ps = {{"mia", 82}, {"ali", 95}, {"zoe", 82}, {"ben", 70}, {"cal", 95}};
            for (auto& p : rankPlayers(ps)) cout << p.name << " " << p.score << "\\n";
        }
    """,
    "c": """
        int main(void) {
            Player ps[] = {{"mia", 82}, {"ali", 95}, {"zoe", 82}, {"ben", 70}, {"cal", 95}};
            rankPlayers(ps, 5);
            for (int i = 0; i < 5; i++) printf("%s %d\\n", ps[i].name, ps[i].score);
            return 0;
        }
    """,
}

VERSION = {
    "python": """
        from functools import cmp_to_key


        def compare_versions(a, b):
            xs = [int(p) for p in a.split(".")]                     #@parse
            ys = [int(p) for p in b.split(".")]                     #@parse
            for i in range(max(len(xs), len(ys))):                  #@each
                x = xs[i] if i < len(xs) else 0                     #@pad
                y = ys[i] if i < len(ys) else 0                     #@pad
                if x != y:                                          #@decide
                    return -1 if x < y else 1                       #@decide
            return 0                                                #@equal


        def sort_versions(versions):
            return sorted(versions, key=cmp_to_key(compare_versions))  #@sort
    """,
    "java": """
        static int compareVersions(String a, String b) {
            String[] xs = a.split("\\\\."), ys = b.split("\\\\.");      //@parse
            for (int i = 0; i < Math.max(xs.length, ys.length); i++) { //@each
                int x = i < xs.length ? Integer.parseInt(xs[i]) : 0;    //@pad
                int y = i < ys.length ? Integer.parseInt(ys[i]) : 0;    //@pad
                if (x != y) return x < y ? -1 : 1;                  //@decide
            }
            return 0;                                               //@equal
        }

        static String[] sortVersions(String[] versions) {
            String[] out = versions.clone();                        //@sort
            Arrays.sort(out, (a, b) -> compareVersions(a, b));      //@sort
            return out;                                             //@sort
        }
    """,
    "cpp": """
        int compareVersions(const string& a, const string& b) {
            size_t i = 0, j = 0;                                    //@parse
            while (i < a.size() || j < b.size()) {                  //@each
                long x = 0, y = 0;                                  //@pad
                while (i < a.size() && a[i] != '.') x = x * 10 + (a[i++] - '0');   //@parse
                while (j < b.size() && b[j] != '.') y = y * 10 + (b[j++] - '0');   //@parse
                if (x != y) return x < y ? -1 : 1;                  //@decide
                i++;                                                //@each
                j++;                                                //@each
            }
            return 0;                                               //@equal
        }

        vector<string> sortVersions(vector<string> versions) {
            stable_sort(versions.begin(), versions.end(), [](const string& a, const string& b) {  //@sort
                return compareVersions(a, b) < 0;                   //@sort
            });
            return versions;                                        //@sort
        }
    """,
    "c": """
        int compareVersions(const char* a, const char* b) {
            while (*a || *b) {                                      //@each
                long x = 0, y = 0;                                  //@pad
                while (*a && *a != '.') x = x * 10 + (*a++ - '0');  //@parse
                while (*b && *b != '.') y = y * 10 + (*b++ - '0');  //@parse
                if (x != y) return x < y ? -1 : 1;                  //@decide
                if (*a) a++;                                        //@each
                if (*b) b++;                                        //@each
            }
            return 0;                                               //@equal
        }

        static int byVersion(const void* x, const void* y) {
            return compareVersions(*(const char* const*)x, *(const char* const*)y);  //@sort
        }

        void sortVersions(const char** versions, int n) {
            qsort(versions, n, sizeof(char*), byVersion);           //@sort
        }
    """,
}
VERSION_RUN = {
    "python": """
        print(*sort_versions(["1.10", "1.2", "0.9", "1.2.1", "1.0.0.1"]))
        print(compare_versions("1.2", "1.2.0"), compare_versions("1.10", "1.9"))
    """,
    "java": """
        public static void main(String[] args) {
            System.out.println(String.join(" ", sortVersions(new String[] {"1.10", "1.2", "0.9", "1.2.1", "1.0.0.1"})));
            System.out.println(compareVersions("1.2", "1.2.0") + " " + compareVersions("1.10", "1.9"));
        }
    """,
    "cpp": """
        int main() {
            auto v = sortVersions({"1.10", "1.2", "0.9", "1.2.1", "1.0.0.1"});
            for (size_t i = 0; i < v.size(); i++) cout << (i ? " " : "") << v[i];
            cout << "\\n" << compareVersions("1.2", "1.2.0") << " " << compareVersions("1.10", "1.9") << "\\n";
        }
    """,
    "c": """
        int main(void) {
            const char* v[] = {"1.10", "1.2", "0.9", "1.2.1", "1.0.0.1"};
            sortVersions(v, 5);
            for (int i = 0; i < 5; i++) printf(i ? " %s" : "%s", v[i]);
            printf("\\n%d %d\\n", compareVersions("1.2", "1.2.0"), compareVersions("1.10", "1.9"));
            return 0;
        }
    """,
}

CLOSE = {
    "python": """
        def by_closeness(nums, target):
            return sorted(nums, key=lambda x: (abs(x - target), x))     #@key
    """,
    "java": """
        static int[] byCloseness(int[] nums, int target) {
            Integer[] boxed = Arrays.stream(nums).boxed().toArray(Integer[]::new);   //@box
            Arrays.sort(boxed, (a, b) -> {                              //@key
                int da = Math.abs(a - target), db = Math.abs(b - target);   //@key
                return da != db ? Integer.compare(da, db) : Integer.compare(a, b);  //@key
            });
            return Arrays.stream(boxed).mapToInt(Integer::intValue).toArray();   //@ret
        }
    """,
    "cpp": """
        vector<int> byCloseness(vector<int> nums, int target) {
            sort(nums.begin(), nums.end(), [target](int a, int b) {     //@key
                return make_pair(abs(a - target), a) < make_pair(abs(b - target), b);  //@key
            });
            return nums;                                                //@ret
        }
    """,
    "c": """
        static int target;

        static int byDistance(const void* x, const void* y) {
            int a = *(const int*)x, b = *(const int*)y;                 //@key
            int da = abs(a - target), db = abs(b - target);             //@key
            if (da != db) return (da > db) - (da < db);                 //@key
            return (a > b) - (a < b);                                   //@key
        }

        void byCloseness(int* nums, int n, int t) {
            target = t;                                                 //@box
            qsort(nums, n, sizeof(int), byDistance);                    //@ret
        }
    """,
}
CLOSE_RUN = {
    "python": """
        print(*by_closeness([7, 1, 10, 4, 5, 13], 6))
    """,
    "java": """
        public static void main(String[] args) {
            StringBuilder sb = new StringBuilder();
            for (int x : byCloseness(new int[] {7, 1, 10, 4, 5, 13}, 6)) sb.append(sb.length() > 0 ? " " : "").append(x);
            System.out.println(sb);
        }
    """,
    "cpp": """
        int main() {
            auto v = byCloseness({7, 1, 10, 4, 5, 13}, 6);
            for (size_t i = 0; i < v.size(); i++) cout << (i ? " " : "") << v[i];
            cout << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int a[] = {7, 1, 10, 4, 5, 13};
            byCloseness(a, 6, 6);
            for (int i = 0; i < 6; i++) printf(i ? " %d" : "%d", a[i]);
            printf("\\n");
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

rank_players = py(RANK["python"], "rank_players")
sort_versions = py(VERSION["python"], "sort_versions")
compare_versions = py(VERSION["python"], "compare_versions")
by_closeness = py(CLOSE["python"], "by_closeness")

PLAYERS = [("mia", 82), ("ali", 95), ("zoe", 82), ("ben", 70), ("cal", 95)]
RANKED = rank_players(PLAYERS)
assert [n for n, _ in RANKED] == ["ali", "cal", "mia", "zoe", "ben"]


def names(ps):
    return [f"{n} {s}" for n, s in ps]


# Decisions the comparator makes for a few pairs.
PAIRS = [(("mia", 82), ("ali", 95)), (("ali", 95), ("cal", 95)), (("zoe", 82), ("mia", 82)), (("ben", 70), ("zoe", 82))]


def first_of(a, b):
    if a[1] != b[1]:
        return (a if a[1] > b[1] else b), "higher score first"
    return (a if a[0] < b[0] else b), "same score, so the name decides"


pair_rows = [(f"{a[0]} {a[1]}", f"{b[0]} {b[1]}", first_of(a, b)[0][0], first_of(a, b)[1]) for a, b in PAIRS]

# Two stable passes: by name first, then by score (descending), keeps names in order within each score.
PASS1 = sorted(PLAYERS, key=lambda p: p[0])
PASS2 = sorted(PASS1, key=lambda p: -p[1])
assert PASS2 == RANKED
sw = Steps("The same ranking with two plain sorts, relying on stability. Sort by the *least* important key first. Follow the two pairs of tied players by their colours.")
TIE = {n: ("found" if sc == 95 else "mark") for n, sc in PLAYERS if sc in (95, 82)}


def tie_state(ps):
    return {k: TIE[n] for k, (n, _) in enumerate(ps) if n in TIE}


sw.step("The players as given. Two pairs tie on score: ali and cal on 95, mia and zoe on 82.",
        Row(names(PLAYERS), st=tie_state(PLAYERS), label="players"), M({"pass": "none yet", "sorted by": "–"}))
sw.step("Pass 1: sort by name only. The scores are all over the place, but within each tied pair the names are now in order.",
        Row(names(PASS1), st=tie_state(PASS1), label="players"), M({"pass": "1", "sorted by": "name"}))
sw.step("Pass 2: a *stable* sort by score, highest first. Tied players keep the order pass 1 gave them, so ali stays before cal and mia before zoe.",
        Row(names(PASS2), st=tie_state(PASS2), label="players"), M({"pass": "2", "sorted by": "score (stable)"}), result=" ".join(n for n, _ in PASS2))
SW_LEGEND = {"found": "tied on 95", "mark": "tied on 82"}

# The sort only ever asks the comparator one question. Insertion sort, every question shown.
iw = Steps("Insertion sort with the ranking rule. Every step is one question to the comparator: \"does this player go before that one?\"")
arr = list(PLAYERS)
asked = 0
iw.step("The first player on its own is already \"sorted\". Each later player moves left past everyone the rule puts after it.",
        Row(names(arr), st={0: "found"}, label="players"), M({"question": "–", "answer": "–", "questions so far": 0}))
for i in range(1, len(arr)):
    j = i
    while j > 0:
        x, y = arr[j], arr[j - 1]
        winner, _ = first_of(x, y)
        why = (f"{winner[0]} has the higher score" if x[1] != y[1] else f"same score, and {winner[0]} comes first by name")
        asked += 1
        q = f"{x[0]} {x[1]} before {y[0]} {y[1]}?"
        st = {**{k: "found" for k in range(i + 1) if k not in (j, j - 1)}, j: "active", j - 1: "mark"}
        if winner == x:
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            iw.step(f"Is {x[0]} ({x[1]}) before {y[0]} ({y[1]})? Yes: {why}. Swap them; {x[0]} keeps moving left.",
                    Row(names(arr), st={**{k: "found" for k in range(i + 1) if k not in (j, j - 1)}, j - 1: "active", j: "mark"}, label="players"),
                    M({"question": q, "answer": "yes", "questions so far": asked}))
            j -= 1
        else:
            iw.step(f"Is {x[0]} ({x[1]}) before {y[0]} ({y[1]})? No: {why}. {x[0]} stops here.",
                    Row(names(arr), st=st, label="players"), M({"question": q, "answer": "no", "questions so far": asked}))
            break
assert arr == RANKED
iw.step(f"Everyone is in place after {asked} questions. The sort itself knows nothing about scores or names: it only ever asked the rule.",
        Row(names(arr), st={k: "found" for k in range(len(arr))}, label="players"), M({"question": "–", "answer": "–", "questions so far": asked}), result=" ".join(n for n, _ in arr))
IW_LEGEND = {"found": "already in order by the rule", "active": "the player moving left", "mark": "the player it's compared with"}

# Version comparison, part by part.
VA, VB = "1.2.1", "1.10"
vw = Steps(f"`compare_versions(\"{VA}\", \"{VB}\")`. Compare the numbers between the dots, left to right.")
xs, ys = [int(p) for p in VA.split(".")], [int(p) for p in VB.split(".")]
vw.step(f"Split at the dots: {xs} and {ys}. Compare them as numbers: 10 is bigger than 2, even though the text \"10\" sorts before \"2\".",
        Row(xs, label=VA), Row(ys, label=VB))
for i in range(max(len(xs), len(ys))):
    x = xs[i] if i < len(xs) else 0
    y = ys[i] if i < len(ys) else 0
    if x != y:
        vw.step(f"Part {i}: {x} vs {y}. They differ, so this decides it: {VA if x < y else VB} is the smaller version.",
                Row(xs, st={i: "active"}, label=VA), Row(ys, st={i: "active"}, label=VB), result=-1 if x < y else 1)
        break
    vw.step(f"Part {i}: {x} vs {y}. Equal, so move on to the next part.", Row(xs, st={i: "found"}, label=VA), Row(ys, st={i: "found"}, label=VB))
VERS = ["1.10", "1.2", "0.9", "1.2.1", "1.0.0.1"]
VSORTED = sort_versions(VERS)
TEXT_SORTED = sorted(VERS)
assert VSORTED == ["0.9", "1.0.0.1", "1.2", "1.2.1", "1.10"] and VSORTED != TEXT_SORTED
assert compare_versions("1.2", "1.2.0") == 0

CLOSE_IN, CLOSE_T = [7, 1, 10, 4, 5, 13], 6
CLOSE_OUT = by_closeness(CLOSE_IN, CLOSE_T)
close_rows = [(str(x), str(abs(x - CLOSE_T)), f"({abs(x - CLOSE_T)}, {x})") for x in CLOSE_OUT]

# A comparator that breaks the rules: rock beats scissors beats paper beats rock.
RPS = {"rock": "scissors", "scissors": "paper", "paper": "rock"}

# Ranking map example (custom alphabet of sizes).
SIZES = ["M", "XS", "L", "S", "XL", "M", "S"]
SIZE_ORDER = ["XS", "S", "M", "L", "XL"]
SIZE_RANK = {s: i for i, s in enumerate(SIZE_ORDER)}
SIZES_SORTED = sorted(SIZES, key=SIZE_RANK.__getitem__)

lesson(
    "sorting",
    "custom-order",
    """
    Sorting isn't only "smallest first". You can sort by any rule you can state: by score and then by name, by
    distance from a target, by version number, by a ranking list someone hands you. Turn the rule into a key (a value
    to sort by) or a comparator (a function that says which of two items goes first), and the library sort does
    the rest.
    """,
    [
        ("idea", "The idea", [
            """
            A sort only ever asks one question: "should `a` go before `b`?". Merge sort, quick sort, Timsort, all of them
            build the whole order out of answers to that question. Usually the answer is "if `a < b`", but nothing stops
            you answering it any way you like.

            Think of a race organiser ranking runners. Fastest time first; if two runners tied, the one with the lower
            bib number first. That rule fits on one line, and once it's written down, the sorting itself is somebody
            else's job.

            There are two ways to hand the rule over:

            - A key: turn each item into a value that already sorts the right way, such as the pair
              `(time, bib)`. Pairs (tuples) compare their first parts, and only look at the second part on a tie.
            - A comparator: a function `compare(a, b)` that returns negative if `a` goes first, positive if `b`
              does, and 0 if they tie.
            """,
            fig(Row(names(PLAYERS), label="as given"), Row(names(RANKED), label="highest score first, ties by name"),
                caption="One sort, one rule: score descending, then name ascending."),
            key("""
            Write the rule as "first by …, then by …". Encode it as a key tuple (negate a number to flip its direction)
            or as a comparator that checks the keys in order and returns at the first difference. As long as the rule is
            consistent, the library sort can use it.
            """),
        ]),
        ("signals", "When to reach for it", [
            """
            The question describes an order that isn't plain ascending: "sort by frequency, then by value", "order the
            logs so letters come before digits", "rank teams by votes, breaking ties by…", "arrange to form the largest
            number", "in the order given by this list". Also any problem where the clever part is *choosing what to sort
            by* before a simple scan, such as sorting intervals by end time, or people by height so the tallest are
            placed first.

            Choosing between a key and a comparator:
            """,
            table(["the rule is…", "use", "example"],
                  ["a list of fields to compare in order", "a key tuple", "(-score, name)"],
                  ["a value computed from each item", "a key", "(distance to target, value)"],
                  ["\"where does it sit in this list\"", "a key from a rank map", "rank[size]"],
                  ["only defined between two items", "a comparator", "version strings, \"which concatenation is bigger\""]),
            """
            Not a fit: when you only need the top few items (*Quickselect* or a heap), or when the keys are small
            integers and you need linear time (*Counting and bucket sort*).
            """,
        ]),
        ("theory", "Why it works", [
            """
            ### Tuples compare left to right

            `(95, "cal")` versus `(95, "ali")`: the first parts tie, so the second parts decide, and `"ali"` wins.
            `(82, "zoe")` versus `(95, "ali")`: the first parts differ, so the second parts are never looked at. That's
            "first by score, then by name". Most languages compare tuples, pairs, arrays or records this way, so a key
            tuple is the quickest way to write a rule with several levels.

            To flip one level, flip its value: `-score` for numbers. For strings you can't negate, so either use a
            comparator for that level or sort in two stable passes (below).

            Here are some of the decisions the ranking rule makes:
            """,
            table(["a", "b", "goes first", "why"], *pair_rows),
            """
            ### What a comparator must promise

            A sort trusts the comparator completely, so the comparator has to describe a real order:

            - nothing goes before itself (`compare(a, a)` is 0);
            - it's consistent: if `a` goes before `b`, then `b` doesn't go before `a`;
            - it's **transitive**: if `a` goes before `b` and `b` before `c`, then `a` goes before `c`, and ties
              chain the same way.

            Break these and the sort may return garbage, loop, or (in Java) throw "Comparison method violates its general
            contract!". Rock-paper-scissors is the classic broken rule: rock beats scissors, scissors beat paper, paper
            beats rock. There's no correct order to produce, so different sorts give different answers.

            A comparator that compares fields one at a time and returns at the first difference is always fine, because
            it's just a tuple comparison written out by hand.

            ### Stability lets you sort in passes

            A stable sort keeps tied items in the order they arrived. So you can build a multi-level order by sorting
            once per level, starting with the *least* important key. Whatever order the earlier passes made survives
            inside each tie of the later passes.
            """,
            walk(sw, legend=SW_LEGEND),
            """
            That's handy when one level is "descending" for a type you can't negate, or when the levels are chosen at
            runtime (a table whose user clicks on column headers).

            ### Keys are computed once; comparators run every time

            A sort makes about `n log n` comparisons. With a comparator, any work inside it (parsing a string, computing
            a distance) happens on every comparison. With a key, Python computes it once per item and keeps it. In other
            languages you can get the same effect yourself by computing the keys first into an array of pairs (key, item)
            and sorting that. This is called decorate, sort, undecorate.
            """,
        ]),
        ("template", "The template", [
            "Rank players by score, highest first, breaking ties alphabetically by name.",
            code(
                "Sort by several keys",
                RANK,
                [
                    ("copy", "Sort a copy, so the caller's list is left as it was."),
                    ("key", "The rule: score descending, then name ascending.",
                     {"python": "A key tuple. `-p[1]` flips the score so higher comes first; `p[0]` breaks ties.",
                      "java": "`comparingInt(...).reversed()` for score descending, then `thenComparing` for the name. The explicit `(Player p)` type helps Java infer the chain.",
                      "cpp": "A lambda that answers \"does `a` go strictly before `b`?\".",
                      "c": "`qsort` passes pointers to the two elements as `void*`; cast them back."}),
                    ("first", "Different scores: the higher one goes first, and that's the end of it."),
                    ("second", "Same score: compare names.",
                     {"c": "`strcmp` already returns negative, zero or positive, exactly the comparator convention."}),
                    ("ret", "The ranked players.", {"c": "C sorts the caller's array in place."}),
                ],
                RANK_RUN,
                "rank_players([(\"mia\", 82), (\"ali\", 95), (\"zoe\", 82), (\"ben\", 70), (\"cal\", 95)])",
            ),
        ]),
        ("trace", "Trace it by hand", [
            """
            To check a custom order by hand, write the key next to each item and sort the keys in your head. For the
            players the keys are `(-95, "ali")`, `(-95, "cal")`, `(-82, "mia")`, `(-82, "zoe")` and `(-70, "ben")`, which is
            already the right order. If the keys come out in the right order, the items will too.

            Whatever sort the library uses, all it does is ask your rule about two items at a time. Here's that on the
            players, using insertion sort because it's the easiest to follow:
            """,
            walk(iw, legend=IW_LEGEND),
            """
            A rule that *can't* be written as a key is traced the same way, one pair at a time. Version numbers are
            the standard example:
            """,
            walk(vw, legend={"found": "equal part: look further right", "active": "the first part that differs: it decides"}),
        ]),
        ("examples", "More examples", [
            f"""
            ### Version numbers

            Sorting `{VERS}` as text gives `{TEXT_SORTED}`, which is wrong: text compares character by character,
            so "1.10" sorts before "1.2". Comparing the parts as numbers gives `{VSORTED}`. And "1.2" and "1.2.0" are
            the same version: missing parts count as 0.

            ### Closest to a target

            Order `{CLOSE_IN}` by how close each number is to {CLOSE_T}, smaller numbers first on a tie. The key is
            `(distance, value)`:
            """,
            table(["value", "distance to 6", "key"], *close_rows),
            f"""
            ### An order someone hands you

            Clothes sizes don't sort alphabetically. Write the order down once, `{SIZE_ORDER}`, and turn it into a rank
            map: each size to its position. Then sort by `rank[size]`: `{SIZES}` becomes `{SIZES_SORTED}`. Decide up front
            what happens to items the list doesn't mention (put them at the end, or reject them).

            ### Picking the order

            In many problems the sort is one line, and the hard part is working out *which* order makes the rest easy.
            Sorting meetings by start time lets you sweep through them; sorting people tallest first means each one
            only has to fit among people at least as tall; sorting pieces by "which concatenation is bigger" makes a
            greedy choice correct. When you see a hard ordering problem, ask: "if the input were sorted by *something*,
            would a single pass solve it?"
            """,
        ]),
        ("variations", "Variations", [
            """
            ### A comparator that isn't a key

            You could turn version strings into tuples of numbers, but comparing them part by part is just as easy, and
            the same shape works for any rule that's defined between two items. The comparator returns negative, zero or
            positive, and pads the shorter version with zeros.
            """,
            code(
                "Compare and sort version numbers",
                VERSION,
                [
                    ("parse", "Read the numbers between the dots.",
                     {"java": "`split` takes a regular expression, and `.` means \"any character\", so it's escaped as `\\\\.`.",
                      "cpp": "Build each part digit by digit while walking the string.",
                      "c": "Walk both strings with pointers, building each part digit by digit."}),
                    ("each", "Compare part by part, until both versions are used up.",
                     {"cpp": "Step past the dot (or past the end, which is harmless here).",
                      "c": "Step past the dot, but never past the string's end."}),
                    ("pad", "A missing part counts as 0, so \"1.2\" equals \"1.2.0\"."),
                    ("decide", "The first part that differs decides."),
                    ("equal", "Every part matched: the versions are equal."),
                    ("sort", "Sort with the comparator.",
                     {"python": "`cmp_to_key` wraps a two-argument comparator so `sorted` can use it.",
                      "java": "Sorting an array of objects with a comparator uses a stable merge sort (Timsort).",
                      "cpp": "`stable_sort` keeps equal versions in their input order; the lambda turns the three-way result into \"goes first?\".",
                      "c": "The array holds `char*` pointers, so `qsort` hands the comparator pointers to pointers."}),
                ],
                VERSION_RUN,
                "sort_versions([\"1.10\", \"1.2\", \"0.9\", \"1.2.1\", \"1.0.0.1\"]); compare(\"1.2\", \"1.2.0\"); compare(\"1.10\", \"1.9\")",
            ),
            """
            ### A computed key

            When the order depends on a value you work out from each item, sort by that value, with the item itself as a
            tie-breaker so the result is fully determined.
            """,
            code(
                "Sort by distance to a target",
                CLOSE,
                [
                    ("box", "Set up what the comparator needs.",
                     {"java": "`Arrays.sort` with a comparator needs objects, so box the `int`s first.",
                      "c": "`qsort`'s comparator can't take extra arguments, so the target goes in a file-level variable."}),
                    ("key", "Order by distance first, then by the value itself.",
                     {"python": "The key `(abs(x - target), x)` is computed once per value.",
                      "java": "`Integer.compare` rather than subtraction, which can overflow.",
                      "cpp": "`make_pair` compares like a tuple: distance first, value second.",
                      "c": "`(a > b) - (a < b)` gives -1, 0 or 1 without any risk of overflow."}),
                    ("ret", "The values, closest first."),
                ],
                CLOSE_RUN,
                "by_closeness([7, 1, 10, 4, 5, 13], target=6)",
            ),
        ]),
        ("complexity", "What it costs", [
            """
            Sorting with a custom rule is still O(n log n) comparisons. What changes is the cost of one comparison. A key
            tuple of small fields is O(1); comparing two strings is O(length); a comparator that parses its inputs pays
            that parsing on every one of the `n log n` calls. Precomputing keys (decorate, sort, undecorate) costs O(n)
            extra memory and makes each comparison cheap again.
            """,
            table(
                ["Approach", "Time", "Extra space"],
                ["Key tuple (computed once per item)", "O(n log n) comparisons + n key computations", "O(n) for the keys"],
                ["Comparator doing work each call", "O(n log n) × the cost of that work", "O(1)"],
                ["One stable pass per level, k levels", "O(k · n log n)", "as the sort"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            `sorted(items, key=...)` and `list.sort(key=..., reverse=True)`. Keys are computed once per item. Tuples
            compare left to right. For a two-argument comparator, wrap it with `functools.cmp_to_key`. The sort is stable,
            so passes work.

            ### Java

            `list.sort(comparator)` or `Arrays.sort(array, comparator)` for objects (stable). Build comparators with
            `Comparator.comparing`, `comparingInt`, `thenComparing` and `reversed()`. Never write `(a, b) -> a - b`: it
            overflows for large or negative values. Use `Integer.compare(a, b)`. Primitive `int[]` can't take a comparator;
            box to `Integer[]` or sort indices.

            ### C++

            `std::sort(first, last, less)` where `less(a, b)` returns true only if `a` must come *strictly* before `b`.
            Returning true for equal items (writing `<=`) breaks the sort and is undefined behaviour. `std::tie` or
            `make_pair` compare like tuples. `std::sort` isn't stable; `std::stable_sort` is.

            ### C

            `qsort(base, n, size, cmp)` with `int cmp(const void*, const void*)` returning negative, zero or positive.
            The comparator can't take extra arguments, so pass extra data through a file-level variable. `qsort` isn't
            guaranteed to be stable: add a final tie-breaker (such as the original index) when the order of ties matters.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - Comparators written as `a - b`, which overflow on large or negative numbers.
            - Comparators that aren't consistent or transitive. Java may throw; C++ may crash or misbehave.
            - `<=` in a C++ "less" function.
            - Sorting numbers stored as strings: `"10"` sorts before `"9"`.
            - Forgetting a final tie-breaker, so the output depends on which sort the library used.
            - Multi-pass sorting with an unstable sort (or doing the passes in the wrong order: least important first).
            - Expensive work inside a comparator that runs `n log n` times.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("How do you sort by score descending, then name ascending, with one key?",
                 "Use the tuple (-score, name). Tuples compare the first part, and only look at the second on a tie."),
                ("You want the same order using two sorts. Which key do you sort by first, and what must be true of the sort?",
                 "Sort by name first (the least important key), then by score. The second sort must be stable, so equal scores keep their name order."),
                ("Why is `(a, b) -> a - b` a bad comparator?",
                 "The subtraction can overflow: with a large positive a and a large negative b, a - b wraps to a negative number and the order flips."),
                ("Why does sorting [\"1.10\", \"1.2\"] as text give the wrong version order?",
                 "Text compares character by character: '1' = '1', '.' = '.', then '1' < '2'. It never sees that 10 > 2 as numbers."),
                ("What goes wrong with the rule 'rock beats scissors, scissors beat paper, paper beats rock'?",
                 "It isn't transitive, so no order satisfies it. A sort given this comparator can return any arrangement, or fail."),
            ),
        ]),
    ],
)
