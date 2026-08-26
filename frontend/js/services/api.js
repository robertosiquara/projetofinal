import { API_BASE_URL } from "../config/constants.js";
import { authStorage } from "../utils/storage.js";

export class ApiError extends Error {
  constructor(message, status = 0, details = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.details = details;
  }
}

async function parseResponse(response) {
  if (response.status === 204) return null;
  const type = response.headers.get("content-type") ?? "";
  return type.includes("application/json") ? response.json() : null;
}

export async function apiRequest(path, options = {}) {
  const headers = new Headers(options.headers);
  const token = authStorage.getToken();
  if (token) headers.set("Authorization", `Bearer ${token}`);

  if (
    options.body &&
    !(options.body instanceof FormData) &&
    !headers.has("Content-Type")
  ) {
    headers.set("Content-Type", "application/json");
  }

  let response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers });
  } catch {
    throw new ApiError("Não foi possível conectar ao servidor.");
  }

  const data = await parseResponse(response);
  if (response.status === 401) {
    authStorage.clear();
    if (!location.pathname.endsWith("index.html")) {
      location.href = "/frontend/index.html";
    }
    throw new ApiError("Sua sessão expirou.", 401, data);
  }

  if (!response.ok) {
    throw new ApiError(
      data?.detail ?? "Não foi possível concluir a operação.",
      response.status,
      data,
    );
  }

  return data;
}
