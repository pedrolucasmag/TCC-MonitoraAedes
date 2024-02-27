(() => {
  function setMapContent(data, removeMap = false) {
    const getRandomOffset = () => Math.random() * 0.0002 - 0.0001;

    function getMarkerIcon(type) {
      return {
        iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-${
          type === "denuncia" ? "red" : type === "visita" ? "gold" : "orange"
        }.png`,
        shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41],
      };
    }

    const filterByXDays = (occurrences, days) => {
      const cutoffDate = new Date();
      cutoffDate.setDate(cutoffDate.getDate() - days);
      return occurrences.filter((data) => new Date(data.create_date) >= cutoffDate);
    };

    function formatarTipoDeManifestacao(valor) {
      return (
        {
          manha: "visita: manhã",
          zika: "contaminação: Zika",
          dengue: "contaminação: Dengue",
          febreamarela: "contaminação: Febre Amarela",
        }[valor] || "Denúncia"
      );
    }

    function getMarkers(occurrences) {
      return occurrences.map((d) => {
        return {
          name: `${d.name}<br>tel: 
                  ${d.tel}<br>${d.rua} - 
                  ${d.numero}<br>
                  ${d.bairro}<br>
                  ${formatarTipoDeManifestacao(d.valortipomanifest)}`,
          location: [d.lat + getRandomOffset(), d.long + getRandomOffset()],
          markerIcon: getMarkerIcon(d.tipomanifest),
        };
      });
    }

    function appendMarkersToMap(map, occurrences) {
      const getOccurrencesMarkers = getMarkers(occurrences);
      const markers = L.markerClusterGroup();

      getOccurrencesMarkers.forEach((m) => {
        const marker = L.marker(m.location, { icon: L.icon(m.markerIcon) });
        marker.bindPopup(m.name);
        markers.addLayer(marker);
      });

      map.addLayer(markers);
    }

    function setMap(occurrences) {
      const [startLat, startLong] = [data[0].lat, data[0].long];
      const map = L.map("map", {
        minZoom: 11,
        dragging: !L.Browser.mobile,
        fullscreenControl: true,
        fullscreenControlOptions: {
          position: "topleft",
        },
      }).setView([startLat, startLong], 14);
      map.attributionControl.setPrefix(false);

      L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      }).addTo(map);

      const thirtyDaysOccurrences = filterByXDays(occurrences, 30);
      appendMarkersToMap(map, thirtyDaysOccurrences);
    }

    setMap(data);
  }

  function setGraphicsContent(data) {
    const defaultOptions = {
      maintainAspectRatio: false,
      responsive: true,
    };

    function getMonthsFromOccurrences(occurrences) {
      const months = [
        "Jan",
        "Fev",
        "Mar",
        "Abr",
        "Mai",
        "Jun",
        "Jul",
        "Ago",
        "Set",
        "Out",
        "Nov",
        "Dez",
      ];

      const occurrences_months = Object.keys(occurrences);
      return months.slice(0, occurrences_months.length);
    }

    function getContaminadosByMonth(occurrences, months, doenca) {
      return months.map((m) => occurrences["contaminados"][doenca]["meses"][m.toLowerCase()]);
    }

    function createChart(chartId, chartType, data, options = defaultOptions) {
      const chart = document.getElementById(chartId).getContext("2d");
      return new Chart(chart, {
        type: chartType,
        data: data,
        options: options,
      });
    }

    function gRegistros(occurrences) {
      const months = getMonthsFromOccurrences(occurrences["ocorrencias"]["meses"]);

      const occurrences_data = months.map(
        (m) => occurrences["ocorrencias"]["meses"][m.toLowerCase()]
      );

      const data = {
        labels: months,
        datasets: [
          {
            label: "Formulários recebidos",
            data: occurrences_data,
            borderWidth: 1,
          },
        ],
      };

      const options = {
        ...defaultOptions,
        scales: {
          y: {
            beginAtZero: true,
          },
        },
        plugins: {
          title: {
            display: true,
            text: `Formulários: ${occurrences["ocorrencias"]["total"]}`,
            font: {
              size: 16,
              weight: "500",
            },
            align: "start",
          },
        },
      };

      return createChart("gRegistros", "bar", data, options);
    }

    function gPossiveisContaminados(occurrences) {
      const months = getMonthsFromOccurrences(occurrences["ocorrencias"]["meses"]);
      const colors = ["#FF6384", "#36A2EB", "#4BC0C0", "#FFCE56"];

      const data = {
        labels: months,
        datasets: ["Dengue", "Zika", "Chikungunya", "Febre Amarela"].map((label, index) => ({
          label,
          data: getContaminadosByMonth(occurrences, months, label.toLowerCase().replace(" ", "")),
          backgroundColor: [colors[index]] + 90,
          borderColor: [colors[index]],
          borderWidth: 1,
        })),
      };

      const options = {
        ...defaultOptions,
        interaction: {
          mode: "index",
          intersect: false,
        },
        stacked: false,
        plugins: {
          title: {
            display: true,
            text: `Total de casos: ${occurrences["contaminados"]["total"]}`,
            font: {
              size: 16,
              weight: "500",
            },
            align: "start",
          },
        },
      };

      return createChart("gContaminados", "line", data, options);
    }

    function gInteresseEmVisitas(occurrences) {
      const visitas = occurrences["visitas"];

      const data = {
        labels: ["MANHÃ", "TARDE"],
        datasets: [
          {
            label: "Interesse em Visitas",
            data: [visitas["manha"], visitas["tarde"]],
            backgroundColor: ["#FF9F40", "#F94144"],
            hoverBackgroundColor: ["#FFC38D", "#FCA5A5"],
          },
        ],
      };

      const options = {
        maintainAspectRatio: false,
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: `Interesses: ${occurrences["visitas"]["total"]}`,
            font: {
              size: 16,
              weight: "500",
            },
            align: "start",
          },
          legend: {
            position: "left",
          },
        },
      };

      return createChart("gInteresseEmVisitas", "doughnut", data, options);
    }

    function gDenuncias(occurrences) {
      const labelData = () => {
        const obj = occurrences["denuncias"];
        const hasBairros = obj["bairros"];
        const labelName = Object.keys(hasBairros ? obj["bairros"] : obj["ruas"] || {});
        const labelValues = Object.values(hasBairros ? obj["bairros"] : obj["ruas"] || {});
        const labelText = hasBairros ? "Bairros com mais denúncias" : "Ruas com mais denúncias";

        return {
          labelName,
          labelValues,
          labelText: labelName.length ? labelText : "Não há denúncias registradas",
        };
      };

      const data = {
        labels: labelData().labelName,
        datasets: [
          {
            data: labelData().labelValues,
            backgroundColor: ["#FF9F40", "#F94144", "#FDB813", "#9013FE", "#09C4FE"],
            hoverBackgroundColor: ["#FFC38D", "#FCA5A5", "#FFD263", "#A760FE", "#53E3FE"],
          },
        ],
      };

      const options = {
        maintainAspectRatio: false,
        responsive: true,
        plugins: {
          name: "chartDenuncias",
          title: {
            display: true,
            text: `Denúncias: ${occurrences["denuncias"]["total"]}`,
            font: {
              size: 16,
              weight: "500",
            },
            align: "start",
          },
          subtitle: {
            display: true,
            text: labelData().labelText,
            align: "start",
          },
          legend: {
            position: "left",
          },
        },
      };

      return createChart("gDenuncias", "pie", data, options);
    }

    gRegistros(data);
    gPossiveisContaminados(data);
    gInteresseEmVisitas(data);
    gDenuncias(data);
  }

  function setTableContent(data) {
    const occurrencesTable = $("#table-occurrences");

    function setTipoManifestacao(tipo, valor) {
      valor = { manha: "manhã", tarde: "tarde", febreamarela: "febre amarela" }[valor] || valor;

      return tipo == "contaminacao"
        ? `Contamin: ${valor}`
        : tipo == "visita"
        ? `Visita: ${valor}`
        : `Denúncia`;
    }

    function makeOccurrencesTableContent(table, data) {
      $(table).DataTable({
        responsive: true,
        pagingType: "simple_numbers",
        pageButtonLength: 3,
        data: data,
        columns: [
          {
            title: "Data",
            data: "create_date",
            render: function (data, type) {
              if (type === "display" || type === "filter") {
                return new Date(data).toLocaleDateString("pt-BR").replace("/2023", "");
              }
              return data;
            },
          },
          { title: "Nome", data: "name" },
          { title: "Telefone", data: "tel" },
          { title: "Email", data: "email" },
          {
            title: "Rua",
            data: "rua",
            render: function (data, type, row) {
              return `${data}, ${row.numero}`;
            },
          },
          { title: "Bairro", data: "bairro" },
          {
            title: "Tipo",
            data: "tipomanifest",
            render: function (data, type, row) {
              return setTipoManifestacao(data, row.valortipomanifest);
            },
          },
        ],
        language: {
          url: "//cdn.datatables.net/plug-ins/1.10.25/i18n/Portuguese-Brasil.json",
          paginate: {
            previous: "<",
            next: ">",
            last: ">>",
            first: "<<",
          },
        },
      });
    }

    makeOccurrencesTableContent(occurrencesTable, data);
  }

  function fetchContent(bairro = "Todos") {
    url = bairro == "Todos" ? "/api/occurrences" : `/api/occurrences?bairro=${bairro}`;
    fetch(url, {
      method: "GET",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        const occurrences = data["data"];
        const occurrences_info = data["occurrences_info"];

        setMapContent(occurrences);
        setGraphicsContent(occurrences_info);
        setTableContent(occurrences);
      })
      .catch((error) => console.error(error));
  }

  function changeContent(value) {
    if (map && map.remove) {
      map.remove();
    }

    const mapDiv = document.createElement("div");
    const mapContainer = document.querySelector(".map-container");
    mapDiv.setAttribute("id", "map");
    mapContainer.append(mapDiv);

    Chart.helpers.each(Chart.instances, (instance) => instance.destroy());
    $("#table-occurrences").DataTable().destroy();

    fetchContent(value);
  }

  fetchContent();
  const selBairros = document.querySelector("#selBairros");
  selBairros.addEventListener("change", (e) => changeContent(e.target.value));
})();
