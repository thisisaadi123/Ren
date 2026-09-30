// Compare an answer with the expected one, per problem.yaml `checker`.
// custom checkers run checker.py in bulk (see check.mjs); this file covers the rest.

const num = (x) => (typeof x === "bigint" ? x : typeof x === "number" ? x : NaN);

function sameExact(a, b) {
  if (Array.isArray(a) || Array.isArray(b)) {
    return Array.isArray(a) && Array.isArray(b) && a.length === b.length && a.every((x, i) => sameExact(x, b[i]));
  }
  if ((typeof a === "bigint" || typeof a === "number") && (typeof b === "bigint" || typeof b === "number")) {
    // 5 and 5n are the same answer; 5 and 5.0 are too (JSON doesn't keep the difference).
    try {
      return BigInt(a) === BigInt(b);
    } catch {
      return num(a) === num(b);
    }
  }
  return a === b;
}

function sameFloat(a, b, tol) {
  if (Array.isArray(a) || Array.isArray(b)) {
    return Array.isArray(a) && Array.isArray(b) && a.length === b.length && a.every((x, i) => sameFloat(x, b[i], tol));
  }
  const x = Number(a);
  const y = Number(b);
  if (!Number.isFinite(x) || !Number.isFinite(y)) return x === y;
  return Math.abs(x - y) <= tol * Math.max(1, Math.abs(y));
}

const key = (v) => JSON.stringify(v, (_k, x) => (typeof x === "bigint" ? x.toString() : x));

// "unordered": the outer list may come back in any order. Inner lists keep their order;
// anything looser needs a custom checker.
function sameUnordered(a, b) {
  if (!Array.isArray(a) || !Array.isArray(b) || a.length !== b.length) return false;
  const count = new Map();
  for (const x of b) count.set(key(x), (count.get(key(x)) ?? 0) + 1);
  for (const x of a) {
    const k = key(x);
    if (!count.get(k)) return false;
    count.set(k, count.get(k) - 1);
  }
  return true;
}

export function same(checker, actual, expected) {
  switch (checker.type) {
    case "exact":
      return sameExact(actual, expected);
    case "float":
      return sameFloat(actual, expected, checker.tolerance);
    case "unordered":
      return sameUnordered(actual, expected);
    default:
      throw new Error(`same(): ${checker.type} checkers run through checker.py`);
  }
}

export const show = (v, max = 160) => {
  const s = key(v);
  return s.length > max ? `${s.slice(0, max)}… (${s.length} chars)` : s;
};
