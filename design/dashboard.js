// Ren — home after log in / sign up.
// The welcome note, one-click ways into each section, then what each one does.
// The account menu, log out and loading the account live in session.js.
(() => {
  const main = document.getElementById("dash");

  const escapeHtml = (s) =>
    String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);

  /* Welcome note -------------------------------------------------------------- */

  function greeting(user, returning) {
    const full = user.name.trim().replace(/\s+/g, " ");
    const name = full ? `<span class="serif accent-text">${escapeHtml(full)}.</span>` : "";
    document.getElementById("greeting").innerHTML = returning
      ? full ? `Welcome back, ${name}` : `Welcome <span class="serif accent-text">back.</span>`
      : full ? `Welcome to Ren, ${name}` : `Welcome to <span class="serif accent-text">Ren.</span>`;
    document.getElementById("greeting-sub").textContent = returning
      ? "What are we working on today?"
      : "Let's get you ready for your next interview.";
  }

  // Returning = has progress, or has opened this page before in this browser.
  // The first visit is remembered only here (localStorage), like the name.
  function isReturning(user) {
    const key = `ren:seen:${user.id}`;
    try {
      const seen = localStorage.getItem(key) === "1";
      localStorage.setItem(key, "1");
      return Boolean(user.progress) || seen;
    } catch {
      return Boolean(user.progress);
    }
  }

  /* Nav: Resume and Interview jump to their rows here; the one in view is
     marked current. Practice has its own page, so over its row (and at the
     top of the page) Home stays current. */

  function navSpy() {
    const links = [...document.querySelectorAll(".nav-links a, .mobile-menu a")];
    const mark = (id) =>
      links.forEach((a) =>
        a.getAttribute("href") === `#${id}` ? a.setAttribute("aria-current", "page") : a.removeAttribute("aria-current")
      );
    const secs = [...document.querySelectorAll(".sec[id]")];
    const hasLink = (id) => links.some((a) => a.getAttribute("href") === `#${id}`);
    const onScroll = () => {
      if (scrollY < 8) return mark("top");
      // The last section whose top has passed a third of the way down the screen.
      const line = innerHeight / 3;
      // At the very bottom the last section can't reach that line, so it wins.
      const atEnd = innerHeight + scrollY >= document.documentElement.scrollHeight - 2;
      const current = atEnd ? secs.at(-1) : secs.filter((s) => s.getBoundingClientRect().top < line).pop();
      mark(current && hasLink(current.id) ? current.id : "top");
    };
    addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* Load --------------------------------------------------------------------- */

  // Wait for the account and the page (images, fonts) under the loader,
  // then let the page settle in as the loader fades.
  Promise.all([renSession(main), renLoader.page])
    .then(([user]) => {
      greeting(user, isReturning(user));
      navSpy();
      return renLoader.done();
    })
    .then(() => renReveal(main));
})();
