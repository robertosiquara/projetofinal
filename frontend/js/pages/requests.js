import { initializeProtectedPage } from "../app.js";
import { ROLES } from "../config/constants.js";
import { requestService } from "../services/request-service.js";
import { showToast } from "../components/toast.js";
const user=await initializeProtectedPage(); const list=document.querySelector("#requests-list");
function render(items){ list.replaceChildren(...items.map((item)=>{ const li=document.createElement("li"); li.className="list-item"; const c=document.createElement("div"); c.className="list-item__content"; const n=document.createElement("strong"); n.textContent=`${item.equipment_name} (${item.quantity})`; const m=document.createElement("span"); m.className="list-item__meta"; m.textContent=`${item.requested_by_name ?? "Usuário"} • ${item.status}`; c.append(n,m); li.append(c); if(user.role!==ROLES.EMPLOYEE && item.status==="Pendente"){ const a=document.createElement("div"); a.className="list-item__actions"; for(const status of ["Concluído","Recusado"]){ const b=document.createElement("button"); b.className=`button button--small ${status==="Concluído"?"button--success":"button--danger"}`; b.textContent=status; b.dataset.requestId=item.id; b.dataset.status=status; a.append(b); } li.append(a); } return li; })); }
async function load(){ try{ render(await requestService.list()); }catch(error){ showToast(error.message,"error"); }}
list?.addEventListener("click",async(event)=>{ const button=event.target.closest("[data-request-id]"); if(!button)return; try{ await requestService.updateStatus(button.dataset.requestId,button.dataset.status); showToast("Solicitação atualizada.","success"); await load(); }catch(error){ showToast(error.message,"error"); }});
if(user) load();
