function getContainer() {
  let container = document.querySelector(".toast-container");
  if (!container) { container = document.createElement("div"); container.className = "toast-container"; container.setAttribute("aria-live", "polite"); document.body.append(container); }
  return container;
}
export function showToast(message, type = "info") {
  const toast = document.createElement("div"); toast.className = `toast toast--${type}`; toast.textContent = message;
  getContainer().append(toast); setTimeout(() => toast.remove(), 4000);
}
