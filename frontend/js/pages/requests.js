import { initializeProtectedPage } from "../app.js";
import { ROLES } from "../config/constants.js";
import { requestService } from "../services/request-service.js";
import { showToast } from "../components/toast.js";

const user = await initializeProtectedPage();
const list = document.querySelector("#requests-list");

function render(items) {
  list.replaceChildren(
    ...items.map((item) => {
      const li = document.createElement("li");
      li.className = "list-item";

      const content = document.createElement("div");
      content.className = "list-item__content";

      const name = document.createElement("strong");
      name.textContent = `${item.equipment_name} (${item.quantity})`;

      const meta = document.createElement("span");
      meta.className = "list-item__meta";
      meta.textContent = `${item.requested_by_name ?? "Usuário"} • ${item.status}`;

      content.append(name, meta);
      li.append(content);

      if (user.role !== ROLES.EMPLOYEE && item.status === "Pendente") {
        const actions = document.createElement("div");
        actions.className = "list-item__actions";

        for (const status of ["Concluído", "Recusado"]) {
          const button = document.createElement("button");
          button.className = `button button--small ${
            status === "Concluído" ? "button--success" : "button--danger"
          }`;
          button.textContent = status;
          button.dataset.requestId = item.id;
          button.dataset.status = status;
          actions.append(button);
        }

        li.append(actions);
      }

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

list?.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-request-id]");
  if (!button) return;

  try {
    await requestService.updateStatus(
      button.dataset.requestId,
      button.dataset.status,
    );
    showToast("Solicitação atualizada.", "success");
    await load();
  } catch (error) {
    showToast(error.message, "error");
  }
});

if (user) load();
