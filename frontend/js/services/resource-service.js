import { apiRequest } from "./api.js";

export const resourceService = {
  list: () => apiRequest("/resources/"),

  create: (data) =>
    apiRequest("/resources/", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  remove: (id) =>
    apiRequest(`/resources/${id}`, {
      method: "DELETE",
    }),
};
