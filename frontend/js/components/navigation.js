import { ROLES } from "../config/constants.js";
import { authService } from "../services/auth-service.js";

const items = [
  { href: "/frontend/welcome.html", label: "Início", roles: Object.values(ROLES) },
  { href: "/frontend/request_resource.html", label: "Solicitar", roles: Object.values(ROLES) },
  { href: "/frontend/requests.html", label: "Solicitações", roles: Object.values(ROLES) },
  { href: "/frontend/resources.html", label: "Recursos", roles: [ROLES.ADMIN, ROLES.MANAGER] },
  { href: "/frontend/users.html", label: "Usuários", roles: [ROLES.ADMIN] },
  { href: "/frontend/dashboard.html", label: "Dashboard", roles: [ROLES.ADMIN, ROLES.MANAGER] },
  { href: "/frontend/alerts.html", label: "Alertas", roles: [ROLES.ADMIN, ROLES.MANAGER] },
];

export function renderNavigation(user) {
  const nav = document.querySelector("#nav-menu");
  if (!nav) return;

  nav.className = "nav-menu";
  nav.replaceChildren();

  for (const item of items.filter((entry) => entry.roles.includes(user.role))) {
    const link = document.createElement("a");
    link.href = item.href;
    link.textContent = item.label;
    if (location.pathname === item.href) link.setAttribute("aria-current", "page");
    nav.append(link);
  }

  const logout = document.createElement("button");
  logout.type = "button";
  logout.textContent = "Sair";
  logout.addEventListener("click", () => authService.logout());
  nav.append(logout);
}
