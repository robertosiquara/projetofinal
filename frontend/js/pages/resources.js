import { initializeProtectedPage } from "../app.js";
import { resourceService } from "../services/resource-service.js";
import { showToast } from "../components/toast.js";

const user = await initializeProtectedPage();
const form = document.querySelector("#resource-form");
const list = document.querySelector("#resources-list");

function render(items) {
  list.replaceChildren(
    ...items.map((item) => {
      const li = document.createElement("li");
      li.className = "list-item";

      const content = document.createElement("div");
      content.className = "list-item__content";

      const name = document.createElement("strong");
      name.textContent = item.name;

      const meta = document.createElement("span");
      meta.className = "list-item__meta";
      meta.textContent = `${item.type} • ${item.quantity} • ${item.status}`;

      const actions = document.createElement("div");
      actions.className = "list-item__actions";

      const button = document.createElement("button");
      button.className = "button button--danger button--small";
      button.textContent = "Excluir";
      button.dataset.resourceId = item.id;

      content.append(name, meta);
      actions.append(button);
      li.append(content, actions);
      return li;
    }),
  );
}

async function load() {
  try {
    render(await resourceService.list());
  } catch (error) {
    showToast(error.message, "error");
  }
}

form?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(form));
  data.quantity = Number(data.quantity);

  try {
    await resourceService.create(data);
    form.reset();
    showToast("Recurso cadastrado.", "success");
    await load();
  } catch (error) {
    showToast(error.message, "error");
  }
});

list?.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-resource-id]");
  if (!button || !confirm("Excluir este recurso?")) return;

  try {
    await resourceService.remove(button.dataset.resourceId);
    showToast("Recurso excluído.", "success");
    await load();
  } catch (error) {
    showToast(error.message, "error");
  }
});

if (user) load();
