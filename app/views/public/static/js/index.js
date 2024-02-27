(() => {
  const tipoManifestacao = document.querySelector("#tipo-manifest");
  const btnLocalizacao = document.querySelector("#btn-localizacao");
  const formOcorrencia = document.querySelector("form");

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
      formOcorrencia.insertAdjacentElement("beforebegin", alerta);
    }
    alerta.scrollIntoView();
  }

  async function getAddressFromCoordinates(lat, long) {
    return fetch(`/api/getReverseGeocode?lat=${lat}&long=${long}`).then((r) => r.json());
  }

  async function handleFormData(e) {
    e.preventDefault();
    let form = document.querySelector("form");
    let formData = new FormData(form);
    let csrf_token = document.querySelector('input[name="csrf_token"]').value;
    formData.append("csrf_token", csrf_token);

    const response = await fetch("/api/getFormData", { method: "post", body: formData }).then((r) =>
      r.json()
    );

    if (response.message) {
      window.location.href = "/sucesso";
    } else {
      msg = Object.keys(response.data)
        .map((key) => response.data[key])
        .join("\n");

      enviarAlerta(msg);
    }
  }

  function setAddressUsingGeolocation() {
    const cep = document.querySelector("#cep");
    const rua = document.querySelector("#rua");
    const numero = document.querySelector("#numero");
    const bairro = document.querySelector("#bairro");

    if (!navigator.geolocation)
      return alert("Geolocalização não está disponível para este navegador!");
    return navigator.geolocation.getCurrentPosition(async (position) => {
      const addressData = await getAddressFromCoordinates(
        position.coords.latitude,
        position.coords.longitude
      );

      const addressComponents = addressData["address_components"];

      for (let i = 0; i < addressComponents.length; i++) {
        const component = addressComponents[i];
        if (component.types.includes("postal_code")) {
          cep.value = component.long_name.replace("-", "").toString();
        } else if (component.types.includes("route")) {
          rua.value = component.long_name;
        } else if (component.types.includes("street_number")) {
          numero.value = component.long_name;
        } else if (component.types.includes("sublocality")) {
          bairro.value = component.long_name;
        }
      }
    });
  }

  function habilitarFormEndereco() {
    ["#btn-localizacao", "#cep", "#rua", "#numero", "#bairro"].forEach((id) =>
      document.querySelector(id).removeAttribute("disabled")
    );
  }

  function setRequiredInput(type) {
    const inputVisita = document.querySelector("#periodo-visita");
    const inputContamin = document.querySelector("#contaminacao-doenca");

    if (type == "visita") {
      inputVisita.setAttribute("required", "");
      inputContamin.removeAttribute("required");
    } else if (type == "contaminacao") {
      inputVisita.removeAttribute("required");
      inputContamin.setAttribute("required", "");
    } else {
      inputVisita.removeAttribute("required");
      inputContamin.removeAttribute("required");
    }
  }

  function setFormContent(type) {
    habilitarFormEndereco();
    setRequiredInput(type);

    const seletorVisita = document.querySelector("#seletor-visita");
    const seletorContamin = document.querySelector("#seletor-contaminacao");
    const seletorDenuncia = document.querySelector("#seletor-denuncia");

    seletorVisita.classList.toggle("desativado", type !== "visita");
    seletorContamin.classList.toggle("desativado", type !== "contaminacao");
    seletorDenuncia.classList.toggle("desativado", type !== "denuncia");
  }

  tipoManifestacao.addEventListener("change", (e) => setFormContent(e.target.value));
  btnLocalizacao.addEventListener("click", setAddressUsingGeolocation);
  formOcorrencia.addEventListener("submit", (e) => handleFormData(e));
})();
