// Ren — talk to the dev server's auth API (server.js).
// Resolves to { ok, status, data }. Rejects with `offline` when there's no API,
// e.g. when the pages are opened through a static server instead of `npm start`.
window.renApi = async (path, body) => {
  let res;
  try {
    res = await fetch(path, {
      method: body === undefined ? "GET" : "POST",
      headers: body === undefined ? {} : { "Content-Type": "application/json" },
      body: body === undefined ? undefined : JSON.stringify(body),
      credentials: "same-origin",
    });
  } catch {
    throw Object.assign(new Error("offline"), { offline: true });
  }
  const isJson = (res.headers.get("content-type") || "").includes("application/json");
  if (!isJson && res.status !== 204) throw Object.assign(new Error("offline"), { offline: true });
  const data = res.status === 204 ? {} : await res.json();
  return { ok: res.ok, status: res.status, data };
};

// The display name is kept only in this browser (localStorage), keyed by
// account id so two people sharing a browser don't see each other's name.
// Storage can be blocked (private windows), so every access is guarded.
window.renName = {
  get(id) {
    try {
      return localStorage.getItem(`ren:name:${id}`) || "";
    } catch {
      return "";
    }
  },
  set(id, name) {
    try {
      localStorage.setItem(`ren:name:${id}`, name);
    } catch {}
  },
};

window.renApi.offlineMessage = "Can't reach the Ren server. Run npm start, then open localhost:3000.";
