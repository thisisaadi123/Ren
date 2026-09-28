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
