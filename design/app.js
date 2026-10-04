// Ren — shared interactions (nav, reveals, segmented controls, message sequences)
(() => {
  const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Links with no destination yet stay put.
  document.querySelectorAll('a[href="#"]').forEach((a) =>
    a.addEventListener("click", (e) => e.preventDefault())
  );

  // Nav: frosted glass once the page scrolls, mobile menu toggle.
  const nav = document.querySelector(".nav");
  if (nav) {
    const onScroll = () => nav.classList.toggle("scrolled", window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });

    const menuBtn = nav.querySelector(".menu-btn");
    menuBtn?.addEventListener("click", () => {
      const open = nav.classList.toggle("open");
      menuBtn.setAttribute("aria-expanded", String(open));
      menuBtn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
    // A tap on a menu link (often a jump within the page) closes the menu.
    nav.querySelectorAll(".mobile-menu a").forEach((a) =>
      a.addEventListener("click", () => {
        if (!nav.classList.contains("open")) return;
        nav.classList.remove("open");
        menuBtn?.setAttribute("aria-expanded", "false");
        menuBtn?.setAttribute("aria-label", "Open menu");
      })
    );
  }

  // Theme toggle: sits in the nav (or the workspace bar) on every page. The
  // head script has already set data-theme; a click saves an explicit choice,
  // and until then the page follows the system setting.
  const root = document.documentElement;
  const KEY = "ren-theme";
  const saved = () => {
    try {
      return localStorage.getItem(KEY);
    } catch {
      return null;
    }
  };
  const actions = document.querySelector(".nav-actions, .ws-actions");
  if (actions) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "icon-btn theme-btn";
    btn.innerHTML = `
      <svg class="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5Z"/></svg>
      <svg class="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M4.6 4.6l1.4 1.4M18 18l1.4 1.4M2.5 12h2M19.5 12h2M4.6 19.4 6 18M18 6l1.4-1.4"/></svg>`;
    const label = () => {
      const dark = root.dataset.theme === "dark";
      btn.setAttribute("aria-label", dark ? "Switch to light theme" : "Switch to dark theme");
      btn.setAttribute("aria-pressed", String(dark));
    };
    const set = (theme) => {
      root.dataset.theme = theme;
      label();
    };
    btn.addEventListener("click", () => {
      const next = root.dataset.theme === "dark" ? "light" : "dark";
      set(next);
      try {
        localStorage.setItem(KEY, next);
      } catch {}
    });
    matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (e) => {
      if (!saved()) set(e.matches ? "dark" : "light");
    });
    label();
    actions.insertBefore(btn, actions.querySelector(".account") || actions.firstChild);
  }

  // Run `fn` once when `el` first scrolls into view.
  const onVisible = (el, fn, threshold = 0.2) => {
    if (reduceMotion || !("IntersectionObserver" in window)) return fn();
    const io = new IntersectionObserver(
      (entries) => {
        if (entries.some((e) => e.isIntersecting)) {
          io.disconnect();
          fn();
        }
      },
      { threshold, rootMargin: "0px 0px -40px 0px" }
    );
    io.observe(el);
  };

  document.querySelectorAll(".reveal").forEach((el) =>
    onVisible(el, () => el.classList.add("in"), 0.12)
  );

  // Segmented controls: sliding thumb, optional linked panels.
  document.querySelectorAll("[data-seg]").forEach((seg) => {
    const thumb = seg.querySelector(".seg-thumb");
    const tabs = [...seg.querySelectorAll('[role="tab"]')];
    const root = seg.closest("[data-tabs]");

    const place = () => {
      const active = tabs.find((t) => t.getAttribute("aria-selected") === "true") || tabs[0];
      thumb.style.width = `${active.offsetWidth}px`;
      thumb.style.transform = `translateX(${active.offsetLeft}px)`;
    };

    tabs.forEach((tab) =>
      tab.addEventListener("click", () => {
        tabs.forEach((t) => t.setAttribute("aria-selected", String(t === tab)));
        if (root) {
          root.querySelectorAll('[role="tabpanel"]').forEach((p) => {
            p.hidden = p.id !== tab.getAttribute("aria-controls");
          });
        }
        place();
      })
    );

    place();
    // Fonts change button widths once they load.
    document.fonts?.ready.then(place);
    window.addEventListener("resize", place);
  });

  // Message sequences: children appear one by one. data-loop replays them.
  document.querySelectorAll("[data-sequence]").forEach((seq) => {
    const items = [...seq.children];
    const step = Number(seq.dataset.step) || 900;
    const loop = seq.hasAttribute("data-loop");

    if (reduceMotion) {
      items.forEach((el) => el.classList.add("show"));
      return;
    }

    const play = () => {
      items.forEach((el, i) => setTimeout(() => el.classList.add("show"), 250 + i * step));
      if (loop) {
        const total = 250 + items.length * step + 3200;
        setTimeout(() => {
          items.forEach((el) => el.classList.remove("show"));
          setTimeout(play, 600);
        }, total);
      }
    };

    onVisible(seq, play, 0.3);
  });
})();
