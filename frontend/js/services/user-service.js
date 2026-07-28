import { apiRequest } from "./api.js";
export const userService = {
  list: () => apiRequest("/users/"),
  create: (data) => apiRequest("/users/", { method: "POST", body: JSON.stringify(data) }),
  remove: (id) => apiRequest(`/users/${id}`, { method: "DELETE" }),
};
