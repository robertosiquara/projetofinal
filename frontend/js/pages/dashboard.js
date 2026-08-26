import { initializeProtectedPage } from "../app.js";
import { apiRequest } from "../services/api.js";
import { showToast } from "../components/toast.js";

const loadingElement = document.querySelector("#dashboard-loading");
const contentElement = document.querySelector("#dashboard-content");
const errorElement = document.querySelector("#dashboard-error");

function countBy(items, key) {
  return items.reduce((totals, item) => {
    const value = item[key] ?? "Não informado";
    totals[value] = (totals[value] ?? 0) + 1;
    return totals;
  }, {});
}

function setText(selector, value) {
  const element = document.querySelector(selector);
  if (element) element.textContent = String(value);
}

function renderBars(containerSelector, data) {
  const container = document.querySelector(containerSelector);
  if (!container) return;

  container.replaceChildren();
  const entries = Object.entries(data).sort(
    ([labelA, valueA], [labelB, valueB]) =>
      valueB - valueA || labelA.localeCompare(labelB, "pt-BR"),
  );

  if (entries.length === 0) {
    const empty = document.createElement("p");
    empty.className = "empty-state";
    empty.textContent = "Nenhum dado disponível.";
    container.append(empty);
    return;
  }

  const maximum = Math.max(...entries.map(([, value]) => value), 1);

  for (const [label, value] of entries) {
    const row = document.createElement("div");
    row.className = "metric-row";

    const header = document.createElement("div");
    header.className = "metric-row__header";

    const name = document.createElement("span");
    name.textContent = label;

    const total = document.createElement("strong");
    total.textContent = String(value);

    const track = document.createElement("div");
    track.className = "metric-row__track";

    const bar = document.createElement("div");
    bar.className = "metric-row__bar";
    bar.style.width = `${Math.max((value / maximum) * 100, 5)}%`;

    header.append(name, total);
    track.append(bar);
    row.append(header, track);
    container.append(row);
  }
}

function calculateAvailable(resources) {
  return resources.filter((resource) => resource.status === "Disponível").length;
}

function calculatePending(requests) {
  return requests.filter((request) => request.status === "Pendente").length;
}

async function loadDashboard() {
  const user = await initializeProtectedPage();
  if (!user) return;

  try {
    const [stats, resources, requests] = await Promise.all([
      apiRequest("/dashboard/stats"),
      apiRequest("/dashboard/resources"),
      apiRequest("/dashboard/requests"),
    ]);

    setText("#total-crimes", stats.length);
    setText("#total-resources", resources.length);
    setText("#available-resources", calculateAvailable(resources));
    setText("#pending-requests", calculatePending(requests));

    renderBars("#crimes-by-villain", countBy(stats, "villain"));
    renderBars("#crimes-by-neighborhood", countBy(stats, "neighborhood"));
    renderBars("#resources-by-type", countBy(resources, "type"));
    renderBars("#resources-by-status", countBy(resources, "status"));
    renderBars("#requests-by-status", countBy(requests, "status"));

    loadingElement?.setAttribute("hidden", "");
    errorElement?.setAttribute("hidden", "");
    contentElement?.removeAttribute("hidden");
  } catch (error) {
    loadingElement?.setAttribute("hidden", "");
    contentElement?.setAttribute("hidden", "");
    errorElement?.removeAttribute("hidden");
    showToast(error.message, "error");
  }
}

loadDashboard();
