import { apiRequest } from "./api.js";
export const requestService = {
  list: () => apiRequest("/requests/"),
  create: (data) => apiRequest("/requests/", { method: "POST", body: JSON.stringify(data) }),
  updateStatus: (id, status) => apiRequest(`/requests/${id}/status`, { method: "PATCH", body: JSON.stringify({ status }) }),
};
