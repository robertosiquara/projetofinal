import { authService } from "../services/auth-service.js";

const form = document.querySelector("#login-form");

form?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = form.querySelector("button[type='submit']");
  const message = document.querySelector("#login-message");

  button.disabled = true;
  message.textContent = "";
  message.className = "message";

  try {
    await authService.login(
      form.elements.username.value.trim(),
      form.elements.password.value,
    );
    location.href = "/frontend/welcome.html";
  } catch (error) {
    message.textContent = error.message;
    message.className = "message message--error";
  } finally {
    button.disabled = false;
  }
});
