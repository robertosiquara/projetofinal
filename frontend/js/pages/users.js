import { initializeProtectedPage } from "../app.js";
import { userService } from "../services/user-service.js";
import { showToast } from "../components/toast.js";
const user = await initializeProtectedPage();
const form = document.querySelector("#user-form"); const list = document.querySelector("#users-list");
function render(users) {
  list.replaceChildren(...users.map((item) => {
    const li = document.createElement("li"); li.className = "list-item";
    const content = document.createElement("div"); content.className = "list-item__content";
    const name = document.createElement("strong"); name.textContent = item.name;
    const meta = document.createElement("span"); meta.className = "list-item__meta"; meta.textContent = `${item.username} • ${item.role}`;
    const actions = document.createElement("div"); actions.className = "list-item__actions";
    const button = document.createElement("button"); button.className = "button button--danger button--small"; button.textContent = "Excluir"; button.dataset.userId = item.id;
    content.append(name, meta); actions.append(button); li.append(content, actions); return li;
  }));
}
async function load() { try { render(await userService.list()); } catch (error) { showToast(error.message, "error"); } }
form?.addEventListener("submit", async (event) => {
  event.preventDefault(); const data = Object.fromEntries(new FormData(form));
  try { await userService.create(data); form.reset(); showToast("Usuário cadastrado.", "success"); await load(); } catch (error) { showToast(error.message, "error"); }
});
list?.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-user-id]"); if (!button || !confirm("Excluir este usuário?")) return;
  try { await userService.remove(button.dataset.userId); showToast("Usuário excluído.", "success"); await load(); } catch (error) { showToast(error.message, "error"); }
});
if (user) load();
