import { authService } from "./services/auth-service.js";
import { authStorage } from "./utils/storage.js";
import { renderNavigation } from "./components/navigation.js";

export async function initializeProtectedPage() {
  if (!authStorage.getToken()) {
    location.href = "/frontend/index.html";
    return null;
  }

  const user = await authService.me();
  renderNavigation(user);
  return user;
}
