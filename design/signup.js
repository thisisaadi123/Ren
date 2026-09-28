// Ren — sign up form: validation, show/hide password, mock submit
(() => {
  const form = document.getElementById("signup-form");
  const inputs = { email: form.elements.email, password: form.elements.password };
  const rules = {
    email: (v) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()),
    password: (v) => v.length >= 8,
  };
  const touched = new Set();

  const check = (key) => {
    const ok = rules[key](inputs[key].value);
    form.querySelector(`[data-field="${key}"]`).classList.toggle("invalid", !ok);
    inputs[key].setAttribute("aria-invalid", String(!ok));
    return ok;
  };

  // Validate after the first blur, then live while typing.
  Object.keys(inputs).forEach((key) => {
    inputs[key].addEventListener("blur", () => {
      if (inputs[key].value) touched.add(key);
      if (touched.has(key)) check(key);
    });
    inputs[key].addEventListener("input", () => {
      if (touched.has(key)) check(key);
    });
  });

  const toggle = form.querySelector(".toggle-pass");
  toggle.addEventListener("click", () => {
    const show = inputs.password.type === "password";
    inputs.password.type = show ? "text" : "password";
    toggle.setAttribute("aria-pressed", String(show));
    toggle.setAttribute("aria-label", show ? "Hide password" : "Show password");
  });

  // No backend yet: fake a short request, then show the confirmation state.
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const keys = Object.keys(inputs);
    keys.forEach((k) => touched.add(k));
    const firstBad = keys.filter((k) => !check(k))[0];
    if (firstBad) return inputs[firstBad].focus();

    const btn = form.querySelector('button[type="submit"]');
    btn.classList.add("loading");
    btn.querySelector(".label").textContent = "Creating account…";

    setTimeout(() => {
      document.getElementById("success-email").textContent = inputs.email.value.trim();
      document.getElementById("signup-view").hidden = true;
      document.getElementById("success-view").hidden = false;
    }, 1200);
  });
})();
