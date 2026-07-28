import { initializeProtectedPage } from "../app.js";
import { apiRequest } from "../services/api.js";
import { showToast } from "../components/toast.js";

const DISPLAY_TIME = 6000;
const INTERVAL_BETWEEN_ALERTS = 5000;

const alertList = document.querySelector("#alert-list");
const liveOverlay = document.querySelector("#live-alert");
const liveType = document.querySelector("#live-alert-type");
const liveVillain = document.querySelector("#live-alert-villain");
const liveLocation = document.querySelector("#live-alert-location");
const liveCounter = document.querySelector("#live-alert-counter");
const startButton = document.querySelector("#start-monitoring");
const stopButton = document.querySelector("#stop-monitoring");
const audio = document.querySelector("#alert-audio");

let alerts = [];
let currentIndex = 0;
let running = false;
let timerId = null;
let countdownId = null;

function sleep(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

function formatTime(date = new Date()) {
  return new Intl.DateTimeFormat("pt-BR", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  }).format(date);
}

function createHistoryItem(alert, receivedAt = new Date()) {
  const article = document.createElement("article");
  article.className = "alert-history-item";

  const icon = document.createElement("span");
  icon.className = "alert-history-item__icon";
  icon.textContent = "!";
  icon.setAttribute("aria-hidden", "true");

  const content = document.createElement("div");
  content.className = "alert-history-item__content";

  const title = document.createElement("strong");
  title.textContent = alert.type;

  const description = document.createElement("p");
  description.textContent = `${alert.villain} detectado em ${alert.location}.`;

  const time = document.createElement("time");
  time.textContent = `Recebido às ${formatTime(receivedAt)}`;
  time.dateTime = receivedAt.toISOString();

  content.append(title, description, time);
  article.append(icon, content);
  return article;
}

function addToHistory(alert) {
  const empty = alertList?.querySelector(".empty-state");
  empty?.remove();
  alertList?.prepend(createHistoryItem(alert));
}

async function playSiren() {
  if (!audio) return;
  try {
    audio.currentTime = 0;
    await audio.play();
  } catch {
    showToast("Clique em 'Iniciar monitoramento' para liberar o som.", "error");
  }
}

function stopSiren() {
  if (!audio) return;
  audio.pause();
  audio.currentTime = 0;
}

function startCountdown(seconds) {
  let remaining = seconds;
  if (liveCounter) liveCounter.textContent = String(remaining);

  clearInterval(countdownId);
  countdownId = setInterval(() => {
    remaining -= 1;
    if (liveCounter) liveCounter.textContent = String(Math.max(remaining, 0));
    if (remaining <= 0) clearInterval(countdownId);
  }, 1000);
}

async function displayLiveAlert(alert) {
  if (!liveOverlay) return;

  liveType.textContent = alert.type;
  liveVillain.textContent = alert.villain;
  liveLocation.textContent = alert.location;
  liveOverlay.removeAttribute("hidden");
  document.body.classList.add("alert-active");

  startCountdown(Math.ceil(DISPLAY_TIME / 1000));
  await playSiren();
  await sleep(DISPLAY_TIME);

  stopSiren();
  liveOverlay.setAttribute("hidden", "");
  document.body.classList.remove("alert-active");
  addToHistory(alert);
}

async function runAlertSequence() {
  while (running && alerts.length > 0) {
    const alert = alerts[currentIndex];
    await displayLiveAlert(alert);

    currentIndex = (currentIndex + 1) % alerts.length;
    if (!running) break;

    await new Promise((resolve) => {
      timerId = setTimeout(resolve, INTERVAL_BETWEEN_ALERTS);
    });
  }
}

function startMonitoring() {
  if (running || alerts.length === 0) return;
  running = true;
  startButton?.setAttribute("disabled", "");
  stopButton?.removeAttribute("disabled");
  runAlertSequence();
}

function stopMonitoring() {
  running = false;
  clearTimeout(timerId);
  clearInterval(countdownId);
  stopSiren();
  liveOverlay?.setAttribute("hidden", "");
  document.body.classList.remove("alert-active");
  startButton?.removeAttribute("disabled");
  stopButton?.setAttribute("disabled", "");
}

async function initializeAlerts() {
  const user = await initializeProtectedPage();
  if (!user) return;

  try {
    alerts = await apiRequest("/alerts/");

    if (alerts.length === 0) {
      const empty = document.createElement("p");
      empty.className = "empty-state";
      empty.textContent = "Nenhum alerta cadastrado para simulação.";
      alertList?.append(empty);
      startButton?.setAttribute("disabled", "");
      return;
    }

    startButton?.addEventListener("click", startMonitoring);
    stopButton?.addEventListener("click", stopMonitoring);
  } catch (error) {
    showToast(error.message, "error");
    startButton?.setAttribute("disabled", "");
  }
}

initializeAlerts();
