// Child process for the judge: reads { tables, datasets, sql, mode, table } as JSON on
// stdin and writes one result per dataset as JSON on stdout. Running here
// means a runaway query can be killed without touching the server.
import { runAll } from "./engine.mjs";

let input = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (chunk) => (input += chunk));
process.stdin.on("end", () => {
  const { tables, datasets, sql, mode, table } = JSON.parse(input);
  process.stdout.write(JSON.stringify(runAll(tables, datasets, sql, { mode, table })));
});
