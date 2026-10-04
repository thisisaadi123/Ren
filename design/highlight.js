// Ren — code highlighting shared by the problem page (editor, Solution tab)
// and the pattern lessons: comments, strings, keywords, numbers and calls.
//   renCode.highlight(src, re)   src as HTML, with tokens from a regex below
//   renCode.as(src, lang)        the same for python, java, cpp, c or sql
//   renCode.tokensFor("#" | "//"), renCode.SQL_TOKENS
(() => {
  const esc = (s) =>
    String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);

  const KEYWORDS = [
    "def", "return", "if", "elif", "else", "for", "while", "in", "and", "or", "not", "is", "lambda", "class",
    "import", "from", "as", "with", "try", "except", "finally", "raise", "pass", "break", "continue", "yield",
    "None", "True", "False", "self", "function", "const", "let", "var", "of", "new", "this", "typeof",
    "public", "private", "protected", "static", "final", "int", "long", "double", "float", "char", "boolean",
    "void", "auto", "bool", "string", "vector", "unordered_map", "unordered_set", "map", "set", "pair",
    "null", "nullptr", "true", "false", "func", "range", "package", "struct", "switch", "case", "default",
    "do", "using", "namespace", "template", "typename", "include", "sizeof", "unsigned", "typedef", "enum",
    "extends", "implements", "interface", "throw", "throws", "assert", "del", "nonlocal", "global",
  ].join("|");

  const tokensFor = (comment) =>
    new RegExp(
      [
        `(${comment === "#" ? "#" : "//"}[^\\n]*)`, // 1 comment
        "(\"(?:[^\"\\\\\\n]|\\\\.)*\"|'(?:[^'\\\\\\n]|\\\\.)*')", // 2 string
        `\\b(${KEYWORDS})\\b`, // 3 keyword
        "\\b(\\d+(?:\\.\\d+)?)\\b", // 4 number
        "\\b([A-Za-z_]\\w*)(?=\\()", // 5 function call
      ].join("|"),
      "g"
    );
  const SQL_KEYWORDS = [
    "select", "from", "where", "and", "or", "not", "in", "is", "null", "as", "on", "join", "left", "right", "full",
    "inner", "outer", "cross", "natural", "using", "group", "by", "order", "having", "limit", "offset", "distinct",
    "union", "all", "intersect", "except", "case", "when", "then", "else", "end", "with", "recursive", "over",
    "partition", "rows", "range", "between", "preceding", "following", "current", "row", "unbounded", "asc", "desc",
    "like", "glob", "exists", "values", "cast", "filter", "window", "nulls", "first", "last", "true", "false",
  ].join("|");
  const SQL_TOKENS = new RegExp(
    [
      "(--[^\\n]*)", // 1 comment
      "('(?:[^']|'')*')", // 2 string
      `\\b(${SQL_KEYWORDS})\\b`, // 3 keyword
      "\\b(\\d+(?:\\.\\d+)?)\\b", // 4 number
      "\\b([A-Za-z_]\\w*)(?=\\()", // 5 function call
    ].join("|"),
    "gi"
  );
  const CLASS = [null, "tk-c", "tk-s", "tk-k", "tk-n", "tk-f"];

  const highlight = (src, re) => {
    let out = "";
    let last = 0;
    for (const m of src.matchAll(re)) {
      out += esc(src.slice(last, m.index));
      const group = m.findIndex((g, i) => i > 0 && g !== undefined);
      out += `<span class="${CLASS[group]}">${esc(m[0])}</span>`;
      last = m.index + m[0].length;
    }
    return out + esc(src.slice(last));
  };

  const BY_LANG = { python: tokensFor("#"), other: tokensFor("//") };
  const as = (src, lang) => highlight(src, lang === "sql" ? SQL_TOKENS : lang === "python" ? BY_LANG.python : BY_LANG.other);

  window.renCode = { highlight, as, tokensFor, SQL_TOKENS };
})();
