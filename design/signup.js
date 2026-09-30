// Ren — sign up form: validation, show/hide password, create the account
(() => {
  const form = document.getElementById("signup-form");
  const inputs = { name: form.elements.name, email: form.elements.email, password: form.elements.password };
  const rules = {
    name: (v) => v.trim().length > 0,
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

  // Form-level message (server errors, offline); cleared as soon as they edit.
  const formError = form.querySelector(".form-error");
  const say = (html) => {
    formError.innerHTML = html;
    formError.hidden = !html;
  };
  form.addEventListener("input", () => say(""));

  const btn = form.querySelector('button[type="submit"]');
  const label = btn.querySelector(".label");
  const busy = (on) => {
    btn.classList.toggle("loading", on);
    label.textContent = on ? "Creating account…" : "Create account";
  };

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const keys = Object.keys(inputs);
    keys.forEach((k) => touched.add(k));
    const firstBad = keys.filter((k) => !check(k))[0];
    if (firstBad) return inputs[firstBad].focus();

    say("");
    busy(true);
    try {
      const { ok, status, data } = await renApi("/api/signup", {
        email: inputs.email.value.trim(),
        password: inputs.password.value,
      });
      if (ok) {
        renName.set(data.user.id, inputs.name.value.trim().replace(/\s+/g, " ").slice(0, 40));
        return location.assign("app.html");
      }
      busy(false);
      if (status === 409) {
        say(`${data.error} <a href="login.html">Log in</a>`);
        inputs.email.focus();
      } else {
        say(data.error || "Something went wrong. Try again.");
      }
    } catch (err) {
      busy(false);
      say(renApi.offlineMessage);
    }
  });
})();
