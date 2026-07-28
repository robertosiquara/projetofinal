import { apiRequest } from "./api.js";
import { authStorage } from "../utils/storage.js";
export const authService = {
  async login(username, password) {
    const body = new URLSearchParams({ username, password });
    const data = await apiRequest("/users/token", { method: "POST", body, headers: { "Content-Type": "application/x-www-form-urlencoded" } });
    authStorage.setToken(data.access_token);
    return data;
  },
  me: () => apiRequest("/users/me"),
  logout() { authStorage.clear(); location.href = "/frontend/index.html"; },
};
