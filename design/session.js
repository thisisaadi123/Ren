// Ren — the signed-in shell shared by every page after log in:
// load the account, fill the account menu, wire log out, and show the
// "no server" note when the pages are opened without `npm start`.
(() => {
  /* Account menu + log out --------------------------------------------------- */

  function account(user) {
    const fallback = user.email.split("@")[0];
    const initial = (user.name || fallback).charAt(0).toUpperCase();
    document.querySelectorAll("[data-initial]").forEach((el) => (el.textContent = initial));
    document.querySelector("[data-name]").textContent = user.name || fallback;
    document.querySelector("[data-email]").textContent = user.email;

    const btn = document.querySelector(".account-btn");
    const menu = document.getElementById("account-menu");
    const items = () => [...menu.querySelectorAll('[role="menuitem"]')];
    const open = (on) => {
      menu.hidden = !on;
      btn.setAttribute("aria-expanded", String(on));
    };

    btn.addEventListener("click", () => {
      open(menu.hidden);
      if (!menu.hidden) items()[0].focus();
    });
    document.addEventListener("click", (e) => {
      if (!menu.hidden && !e.target.closest(".account")) open(false);
    });
    menu.addEventListener("keydown", (e) => {
      const list = items();
      const i = list.indexOf(document.activeElement);
      if (e.key === "ArrowDown") list[(i + 1) % list.length].focus();
      else if (e.key === "ArrowUp") list[(i - 1 + list.length) % list.length].focus();
      else if (e.key === "Escape") {
        open(false);
        btn.focus();
      } else return;
      e.preventDefault();
    });
  }

  document.querySelectorAll("[data-logout]").forEach((b) =>
    b.addEventListener("click", async () => {
      try {
        await renApi("/api/logout", {});
      } finally {
        location.replace("/index.html");
      }
    })
  );

  // Fill in and wire the account badge for a signed-in user (also used by
  // pages anyone can open, like the 404 page). Returns the user with the
  // name kept in this browser.
  window.renAccount = (apiUser) => {
    const user = { ...apiUser, name: renName.get(apiUser.id) || apiUser.name };
    if (document.querySelector(".account-btn")) account(user);
    return user;
  };

  /* Load --------------------------------------------------------------------- */

  // A server that never answers counts as no server.
  const TIMEOUT = 10000;
  const me = () =>
    Promise.race([
      renApi("/api/me"),
      new Promise((_, reject) => setTimeout(() => reject(new Error("timeout")), TIMEOUT)),
    ]);

  // Resolves with the signed-in user once the account menu is filled in.
  // Signed out: goes to log in (the loader stays up until the page changes).
  // No server: swaps `main` for a note with a retry and never resolves, so
  // the page's own setup doesn't run.
  window.renSession = (main) =>
    me()
      .then(({ ok, data }) => {
        if (!ok) {
          location.replace("login.html");
          return new Promise(() => {});
        }
        return renAccount(data.user);
      })
      .catch(() => {
        main.classList.add("is-state");
        main.innerHTML = `
          <div class="state">
            <h1>Can't reach the Ren server</h1>
            <p>Run <code>npm start</code> in the project folder, then open <code>localhost:3000</code>.</p>
            <button type="button" class="btn btn-secondary" data-retry>Try again</button>
          </div>`;
        main.querySelector("[data-retry]").addEventListener("click", () => location.reload());
        (window.renLoader ? renLoader.done() : Promise.resolve()).then(() => renReveal(main));
        return new Promise(() => {});
      });

  // Show the page once it's filled in, then let it settle in.
  window.renReveal = (main) => {
    main.removeAttribute("aria-busy");
    main.classList.add("ready");
  };
})();
