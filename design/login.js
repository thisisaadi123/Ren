// Rise — log in: validation, show/hide password, forgot-password flow (no backend yet)
(() => {
  const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  const views = document.querySelectorAll("[data-view]");

  const show = (name) => {
    views.forEach((v) => (v.hidden = v.dataset.view !== name));
    document.querySelector(`[data-view="${name}"] input`)?.focus();
  };

  document.querySelectorAll("[data-go]").forEach((b) =>
    b.addEventListener("click", () => {
      // Carry the typed email over to the reset form.
      if (b.dataset.go === "reset") {
        document.getElementById("reset-email").value = document.getElementById("email").value;
      }
      show(b.dataset.go);
    })
  );

  // Validate a form's fields: after first blur, live while typing, and on submit.
  const validator = (form, rules) => {
    const touched = new Set();
    const check = (name) => {
      const input = form.elements[name];
      const ok = rules[name](input.value);
      form.querySelector(`[data-field="${name}"]`).classList.toggle("invalid", !ok);
      input.setAttribute("aria-invalid", String(!ok));
      return ok;
    };
    Object.keys(rules).forEach((name) => {
      const input = form.elements[name];
      input.addEventListener("blur", () => {
        if (input.value) touched.add(name);
        if (touched.has(name)) check(name);
      });
      input.addEventListener("input", () => touched.has(name) && check(name));
    });
    return () => {
      const names = Object.keys(rules);
      names.forEach((n) => touched.add(n));
      const bad = names.filter((n) => !check(n))[0];
      if (bad) form.elements[bad].focus();
      return !bad;
    };
  };

  // Fake a short request, then move on.
  const submitting = (form, label, then) => {
    const btn = form.querySelector('button[type="submit"]');
    btn.classList.add("loading");
    btn.querySelector(".label").textContent = label;
    setTimeout(then, 1100);
  };

  const login = document.getElementById("login-form");
  const loginValid = validator(login, {
    email: (v) => EMAIL.test(v.trim()),
    password: (v) => v.length > 0,
  });
  login.addEventListener("submit", (e) => {
    e.preventDefault();
    if (loginValid()) submitting(login, "Logging in…", () => show("done"));
  });

  const reset = document.getElementById("reset-form");
  const resetValid = validator(reset, { "reset-email": (v) => EMAIL.test(v.trim()) });
  reset.addEventListener("submit", (e) => {
    e.preventDefault();
    if (!resetValid()) return;
    submitting(reset, "Sending…", () => {
      document.getElementById("sent-email").textContent = reset.elements["reset-email"].value.trim();
      show("sent");
    });
  });

  // Show / hide password
  const toggle = document.querySelector(".toggle-pass");
  const pass = document.getElementById("password");
  toggle.addEventListener("click", () => {
    const visible = pass.type === "password";
    pass.type = visible ? "text" : "password";
    toggle.setAttribute("aria-pressed", String(visible));
    toggle.setAttribute("aria-label", visible ? "Hide password" : "Show password");
  });
})();
