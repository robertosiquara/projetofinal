import { initializeProtectedPage } from "../app.js";

const user = await initializeProtectedPage();

if (user) {
  document.querySelector("#welcome-title").textContent = `Bem-vindo, ${user.name}`;
}
