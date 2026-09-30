// Ren — the loading screen (the .ren-loader element at the top of the page).
// CSS fades it in only after 300ms, so quick loads never see it. Once it has
// shown, it stays for at least MIN_SHOWN ms so it never blinks, then fades
// away as the page settles in. Like a game's loading screen, it shows a tip
// about Ren or interviews, changing every few seconds on a long load.
(() => {
  const el = document.querySelector(".ren-loader");
  const tip = el?.querySelector(".ren-loader-tip");
  const TIPS = [
    "Ren reads your code before it nudges you.",
    "Hint, nudge, explain or solve: you choose how much help you get.",
    "Say your approach out loud before you code. Interviewers listen for it.",
    "Most DSA problems come down to a handful of patterns. Learn the pattern.",
    "In system design, estimate the load first. The rest follows from it.",
    "In SQL rounds, say what each join is for before you write it.",
    "Check your resume against the jobs you want, not jobs in general.",
    "After a mock interview, Ren leaves notes on what to work on next.",
    "練 (ren) means to train until it's second nature.",
  ];
  const TIP_EVERY = 3600;
  const MIN_SHOWN = 600;
  // The page itself: images and fonts. Capped, so one slow image never
  // holds the page hostage.
  const PAGE_CAP = 6000;

  let shownAt = null;
  let closing = null;
  let tipTimer = null;

  // Start on a random tip, then move through the list.
  if (tip) {
    let i = Math.floor(Math.random() * TIPS.length);
    tip.textContent = TIPS[i];
    tipTimer = setInterval(() => {
      tip.classList.add("swap");
      setTimeout(() => {
        i = (i + 1) % TIPS.length;
        tip.textContent = TIPS[i];
        tip.classList.remove("swap");
      }, 300);
    }, TIP_EVERY);
  }

  el?.addEventListener("animationstart", (e) => {
    if (e.animationName === "loader-in") shownAt = performance.now();
  });

  const loaded = new Promise((resolve) =>
    document.readyState === "complete" ? resolve() : addEventListener("load", resolve, { once: true })
  );
  const capped = (p, ms) => Promise.race([p, new Promise((resolve) => setTimeout(resolve, ms))]);

  window.renLoader = {
    // Resolves when the page's images and fonts are in.
    page: capped(Promise.all([loaded, document.fonts?.ready]), PAGE_CAP),

    // Takes the loader away. Resolves when the page should appear: right
    // away if the loader never showed, else as it starts to fade.
    done() {
      if (closing) return closing;
      clearInterval(tipTimer);
      if (!el) return (closing = Promise.resolve());
      if (shownAt === null) {
        el.remove();
        return (closing = Promise.resolve());
      }
      const wait = Math.max(0, shownAt + MIN_SHOWN - performance.now());
      closing = new Promise((resolve) =>
        setTimeout(() => {
          el.animate([{ opacity: getComputedStyle(el).opacity }, { opacity: 0 }], {
            duration: 350,
            easing: "cubic-bezier(0.2, 0.8, 0.2, 1)",
            fill: "forwards",
          }).finished.then(() => el.remove());
          resolve();
        }, wait)
      );
      return closing;
    },
  };
})();
