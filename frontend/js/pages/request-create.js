import { initializeProtectedPage } from "../app.js";
import { requestService } from "../services/request-service.js";
import { showToast } from "../components/toast.js";
const user=await initializeProtectedPage(); const form=document.querySelector("#request-form"); const list=document.querySelector("#own-requests-list");
function render(items){ list.replaceChildren(...items.map((item)=>{ const li=document.createElement("li"); li.className="list-item"; const c=document.createElement("div"); c.className="list-item__content"; const n=document.createElement("strong"); n.textContent=item.equipment_name; const m=document.createElement("span"); m.className="list-item__meta"; m.textContent=`Quantidade: ${item.quantity} • ${item.status}`; c.append(n,m); li.append(c); return li; })); }
async function load(){ try{ render(await requestService.list()); }catch(error){ showToast(error.message,"error"); }}
form?.addEventListener("submit",async(event)=>{ event.preventDefault(); const data=Object.fromEntries(new FormData(form)); data.quantity=Number(data.quantity); try{ await requestService.create(data); form.reset(); showToast("Solicitação enviada.","success"); await load(); }catch(error){ showToast(error.message,"error"); }});
if(user) load();
