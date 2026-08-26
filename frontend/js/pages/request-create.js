import { initializeProtectedPage } from "../app.js";
import { requestService } from "../services/request-service.js";
import { showToast } from "../components/toast.js";

const user = await initializeProtectedPage();
const form = document.querySelector("#request-form");
const list = document.querySelector("#own-requests-list");

function render(items) {
  list.replaceChildren(
    ...items.map((item) => {
      const li = document.createElement("li");
      li.className = "list-item";

      const content = document.createElement("div");
      content.className = "list-item__content";

      const name = document.createElement("strong");
      name.textContent = item.equipment_name;

      const meta = document.createElement("span");
      meta.className = "list-item__meta";
      meta.textContent = `Quantidade: ${item.quantity} • ${item.status}`;

      content.append(name, meta);
      li.append(content);
      return li;
    }),
  );
}

async function load() {
  try {
    render(await requestService.list());
  } catch (error) {
    showToast(error.message, "error");
  }
}

form?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(form));
  data.quantity = Number(data.quantity);

  try {
    await requestService.create(data);
    form.reset();
    showToast("Solicitação enviada.", "success");
    await load();
  } catch (error) {
    showToast(error.message, "error");
  }
});

if (user) load();
