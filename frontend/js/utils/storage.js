import { STORAGE_KEYS } from "../config/constants.js";
export const authStorage = {
  getToken: () => localStorage.getItem(STORAGE_KEYS.token),
  setToken: (token) => localStorage.setItem(STORAGE_KEYS.token, token),
  clear: () => localStorage.removeItem(STORAGE_KEYS.token),
};
