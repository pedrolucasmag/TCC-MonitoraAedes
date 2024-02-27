(() => {
  const formLogin = document.querySelector("form");

  function criarAlerta(msg) {
    const div = document.createElement("div");
    div.classList.add("alert", "alert-warning", "alert-msg");
    div.setAttribute("role", "alert");
    div.textContent = `⚠ ${msg}`;
    return div;
  }

  function enviarAlerta(msg) {
    let alerta = document.querySelector(".alert-msg");
    if (alerta) {
      alerta.textContent = "⚠ " + msg;
    } else {
      alerta = criarAlerta(msg);
      formLogin.insertAdjacentElement("beforebegin", alerta);
    }
    alerta.scrollIntoView();
  }

  async function handleFormData(e) {
    e.preventDefault();
    let form = document.querySelector("form");
    let formData = new FormData(form);
    let csrf_token = document.querySelector('input[name="csrf_token"]').value;
    formData.append("csrf_token", csrf_token);

    const response = await fetch("/api/login", { method: "post", body: formData }).then((r) => r);

    if (response.ok) {
      return (window.location.href = window.location.href + "dashboard");
    } else {
      const responseData = await response.json();
      msg = Object.keys(responseData.data)
        .map((key) => responseData.data[key])
        .join("\n");

      enviarAlerta(msg);
    }
  }

  formLogin.addEventListener("submit", (e) => handleFormData(e));
})();
