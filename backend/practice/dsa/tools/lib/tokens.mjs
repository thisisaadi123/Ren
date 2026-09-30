// Test inputs for the compiled languages (C++, Java, C), as one token stream
// on stdin: each harness reads it without needing a JSON parser.
//
// Token stream: numbers as decimal, bools as 0/1, chars as their code point,
// strings as "<byte length> <bytes>", arrays as "<length> <items...>",
// lists as "<length> <values...> <cycle_at or -1>", trees as "<length>" then "1 v" or "0" per slot.
export function encode(value, type) {
  if (type.endsWith("[]")) {
    const inner = type.slice(0, -2);
    return [String(value.length), ...value.map((v) => encode(v, inner))].join(" ");
  }
  switch (type) {
    case "int":
    case "long":
      return String(value);
    case "double":
      return Number(value).toPrecision(17);
    case "bool":
      return value ? "1" : "0";
    case "char":
      return String(String(value).codePointAt(0));
    case "string":
      return `${Buffer.byteLength(value, "utf8")} ${value}`;
    case "ListNode": {
      const values = Array.isArray(value) ? value : value.values;
      const cycleAt = Array.isArray(value) ? -1 : value.cycle_at ?? -1;
      return [values.length, ...values, cycleAt].join(" ");
    }
    case "TreeNode":
      return [value.length, ...value.map((v) => (v === null ? "0" : `1 ${v}`))].join(" ");
    default:
      throw new Error(`type ${type} isn't supported`);
  }
}

export function encodeTests(tests, meta) {
  const parts = [String(tests.length)];
  for (const t of tests) {
    parts.push(encode(t.id, "string"));
    if (meta.kind === "design") {
      const calls = t.args.calls;
      parts.push(String(calls.length));
      const [, ...ctorArgs] = calls[0];
      meta.design.constructor.params.forEach((p, i) => parts.push(encode(ctorArgs[i], p.type)));
      for (const [name, ...args] of calls.slice(1)) {
        const m = meta.design.methods.find((x) => x.name === name);
        if (!m) throw new Error(`test ${t.id}: unknown method ${name}`);
        parts.push(encode(name, "string"));
        m.params.forEach((p, i) => parts.push(encode(args[i], p.type)));
      }
    } else {
      for (const p of meta.signature.params) parts.push(encode(t.args[p.name], p.type));
    }
  }
  return parts.join("\n") + "\n";
}
