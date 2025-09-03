const API_URL = 'http://localhost:8000';
let token = localStorage.getItem('token');

let crimesChartInstance = null;
let neighborhoodsChartInstance = null;

// Função para decodificar JWT (extrai payload sem verificar assinatura)
function decodeJWT(token) {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(c => {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
        return JSON.parse(jsonPayload);
    } catch (e) {
        return null;
    }
}

// Função para renderizar mensagem de boas-vindas
function renderWelcomeMessage() {
    if (!token) {
        window.location.href = '/frontend/index.html';
        return;
    }
    const payload = decodeJWT(token);
    const userName = payload?.name || payload?.sub || 'Usuário';
    const welcomeElement = document.querySelector('.welcome');
    if (welcomeElement) {
        welcomeElement.textContent = `Bem-vindo, ${userName}!`;
    }
}

// Função para renderizar menu com base no role do usuário
function renderMenu() {
    const navMenu = document.getElementById('nav-menu');
    if (!navMenu) return;

    navMenu.innerHTML = ''; // Limpa o menu
    if (!token) return; // Sem token, não mostra menu (página de login)

    const payload = decodeJWT(token);
    const role = payload && payload.sub === 'batman' ? 'admin' : payload?.role;
    const username = payload?.sub;

    const menuItems = {
        admin: [
            { text: 'Inicio', href: '/frontend/welcome.html' },
            { text: 'Dashboard', href: '/frontend/dashboard.html' },
            { text: 'Alertas', href: '/frontend/alerts.html' },
            { text: 'Cadastro de Usuário', href: '/frontend/users.html' },
            { text: 'Gerenciamento de Recursos', href: '/frontend/resources.html' },
            { text: 'Solicitação de Recursos', href: '/frontend/request_resource.html' },
            { text: 'Recursos Solicitados', href: '/frontend/requests.html' }
        ],
        Gerente: [
            { text: 'Inicio', href: '/frontend/welcome.html' },
            { text: 'Dashboard', href: '/frontend/dashboard.html' },
            { text: 'Cadastro de Usuário', href: '/frontend/users.html' },
            { text: 'Solicitação de Recursos', href: '/frontend/request_resource.html' },
            { text: 'Recursos Solicitados', href: '/frontend/requests.html' }
        ],
        Funcionário: [
            { text: 'Inicio', href: '/frontend/welcome.html' },
            { text: 'Recursos Solicitados', href: '/frontend/requests.html' }
        ]
    };

    const items = username === 'batman' ? menuItems.admin : menuItems[role] || [];
    const ul = document.createElement('ul');
    items.forEach(item => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = item.href;
        a.textContent = item.text;
        li.appendChild(a);
        ul.appendChild(li);
    });

    const logoutLi = document.createElement('li');
    const logoutButton = document.createElement('button');
    logoutButton.textContent = 'Logout';
    logoutButton.className = 'logar'; // Mesma classe dos outros botões
    logoutButton.onclick = logout; // Chama a função logout
    logoutLi.appendChild(logoutButton);
    ul.appendChild(logoutLi);

    navMenu.appendChild(ul);
}

function logout() {
    localStorage.removeItem('token'); // Remove o token
    token = null; // Limpa a variável token
    const navMenu = document.getElementById('nav-menu');
    if (navMenu) navMenu.innerHTML = ''; // Limpa o menu
    window.location.href = '/frontend/index.html'; // Redireciona para login
}

// Função de login
function login(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorElement = document.getElementById('login-error');
    fetch(`${API_URL}/users/token`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `username=${username}&password=${password}`
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Login falhou');
        }
        return response.json();
    })
    .then(data => {
        if (data.access_token) {
            localStorage.setItem('token', data.access_token);
            token = data.access_token;
            renderMenu();
            window.location.href = '/frontend/welcome.html';
        } else {
            if (errorElement) {
                errorElement.textContent = 'Usuário ou senha inválidos';
                errorElement.style.display = 'block';
            } else {
                alert('Usuário ou senha inválidos');
            }
        }
    })
    .catch(error => {
        if (errorElement) {
            errorElement.textContent = 'Erro ao tentar fazer login';
            errorElement.style.display = 'block';
        } else {
            alert('Erro ao tentar fazer login');
        }
        console.error('Erro no login:', error);
    });
}

function fetchWithAuth(url, options = {}) {
    if (!token) {
        alert('Por favor, faça login novamente.');
        window.location.href = '/frontend/index.html';
        return Promise.reject('No token');
    }
    options.headers = { ...options.headers, Authorization: `Bearer ${token}` };
    return fetch(url, options);
}

// Funções para Users
function loadUsers() {
    const list = document.getElementById('usersList');
    if (!list) return;
    fetchWithAuth(`${API_URL}/users/`)
    .then(response => {
        if (response.status === 403) {
            alert('Acesso negado. Apenas administradores podem visualizar usuários.');
            window.location.href = '/frontend/index.html';
            return Promise.reject('Acesso negado');
        }
        if (!response.ok) {
            throw new Error('Erro ao carregar usuários');
        }
        return response.json();
    })
    .then(users => {
        list.innerHTML = '';
        users.forEach(user => {
            const li = document.createElement('li');
            li.innerHTML = `
                <div>
                    <div><i class="fas fa-user" style="color: #f6fa05ff;"></i><strong>   Usuário:</strong> ${user.username}</div>
                    <div><i class="fas fa-shield" style="color: #2c04e0ff;"></i> <strong>   Função:</strong> ${user.role}</div>
                </div>
            `;
            list.appendChild(li);
        });
    })
    .catch(error => {
        console.error('Erro ao carregar usuários:', error);
        list.innerHTML = '<li>Erro ao carregar usuários</li>';
    });
}

if (document.getElementById('userForm')) {
    document.getElementById('userForm').addEventListener('submit', event => {
        event.preventDefault();
        const roleValue = document.getElementById('role').value;
        if (!roleValue) {
            alert('Por favor, selecione um nível de autorização.');
            return;
        }

        const user = {
            name: document.getElementById('name').value,
            username: document.getElementById('username').value,
            password: document.getElementById('password').value,
            role: document.getElementById('role').value
        };
        fetchWithAuth(`${API_URL}/users/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(user)
        })
        .then(response => {
            if (response.status === 403) {
                alert('Acesso negado. Apenas administradores ou gerentes podem criar usuários.');
                window.location.href = '/frontend/index.html';
                return Promise.reject('Acesso negado');
            }
            if (!response.ok) {
                throw new Error('Erro ao criar usuário');
            }
            return response.json();
        })
        .then(() => loadUsers())
        .catch(async error => {
            console.error('Erro ao criar usuário:', error);
            const errorText = await error.text?.();
            alert(`Erro ao criar usuário: ${errorText || 'Erro desconhecido'}`);
        });
    });
}

// Funções para Resources
function loadResources() {
    const list = document.getElementById('resourcesList');
    if (!list) return;

    fetchWithAuth(`${API_URL}/resources/`)
        .then(response => {
            if (response.status === 403) {
                alert('Acesso negado.');
                window.location.href = '/frontend/index.html';
                return Promise.reject('Acesso negado');
            }
            if (!response.ok) {
                throw new Error('Erro ao carregar recursos');
            }
            return response.json();
        })
        .then(resources => {
            list.innerHTML = '';
            resources.forEach(res => {
                const li = document.createElement('li');
                li.className = 'resource-card';
                li.innerHTML = `
                    <div class="resource-line"><strong>ID:</strong> ${res.id}</div>
                    <div class="resource-line"><strong>Nome:</strong> ${res.name}</div>
                    <div class="resource-line"><strong>Tipo:</strong> ${res.type}</div>
                    <div class="resource-line"><strong>Quantidade:</strong> ${res.quantity}</div>
                    <div class="resource-line"><strong>Status:</strong> ${res.status}</div>
                    <div class="resource-line">
                        <button class="logar edit-btn" data-id="${res.id}">Editar</button>
                        <button class="logar delete-btn" data-id="${res.id}">Deletar</button>
                    </div>
                `;
                li.querySelector('.edit-btn').addEventListener('click', () => editResource(res));
                li.querySelector('.delete-btn').addEventListener('click', () => deleteResource(res.id));
                list.appendChild(li);
            });
        })
        .catch(error => {
            console.error('Erro ao carregar recursos:', error);
            list.innerHTML = '<li>Erro ao carregar recursos</li>';
        });
}

function resetForm() {
    const form = document.getElementById('resourceForm');
    form.reset();
    document.getElementById('resource-id').value = '';
    document.getElementById('resource-button').textContent = 'Adicionar Recurso';
}

function editResource(resource) {
    document.getElementById('name').value = resource.name;
    document.getElementById('type').value = resource.type;
    document.getElementById('quantity').value = resource.quantity;
    document.getElementById('resource-id').value = resource.id;
    document.getElementById('resource-button').textContent = 'Enviar edição';
}

function deleteResource(resourceId) {
    if (!confirm('Tem certeza que deseja deletar este recurso?')) return;
    fetchWithAuth(`${API_URL}/resources/${resourceId}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.status === 403) {
            alert('Acesso negado. Apenas administradores podem deletar recursos.');
            window.location.href = '/frontend/index.html';
            return Promise.reject('Acesso negado');
        }
        if (!response.ok) {
            throw new Error('Erro ao deletar recurso');
        }
        loadResources();
    })
    .catch(error => {
        console.error('Erro ao deletar recurso:', error);
        alert('Erro ao deletar recurso');
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const resourceForm = document.getElementById('resourceForm');

    if (resourceForm) {
        resourceForm.addEventListener('submit', event => {
            event.preventDefault();

            const name = document.getElementById('name').value.trim();
            const type = document.getElementById('type').value;
            const quantity = parseInt(document.getElementById('quantity').value);
            const resourceId = document.getElementById('resource-id').value;

            if (!name || !type || isNaN(quantity)) {
                alert('Preencha todos os campos corretamente.');
                return;
            }

            const resource = {
                name: name,
                type: type,
                quantity: quantity,
                status: quantity > 0 ? 'Disponível' : 'Indisponível'
            };

            if (resourceId) {
                // Modo edição
                resource.id = parseInt(resourceId);

                fetchWithAuth(`${API_URL}/resources/${resourceId}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(resource)
                })
                .then(response => {
                    if (!response.ok) {
                        return response.text().then(text => {
                            console.error('❌ Resposta da API:', text);
                            throw new Error('Erro ao editar recurso');
                        });
                    }
                    return response.json();
                })
                .then(() => {
                    loadResources();
                    resetForm();
                })
                .catch(error => {
                    console.error('Erro ao editar recurso:', error);
                    alert('Erro ao editar recurso.');
                });

            } else {
                // Modo criação
                fetchWithAuth(`${API_URL}/resources/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(resource)
                })
                .then(response => {
                    if (!response.ok) {
                        return response.text().then(text => {
                            console.error('❌ Erro na criação:', text);
                            throw new Error('Erro ao criar recurso');
                        });
                    }
                    return response.json();
                })
                .then(() => {
                    loadResources();
                    resetForm();
                })
                .catch(error => {
                    console.error('Erro ao criar recurso:', error);
                    alert('Erro ao criar recurso.');
                });
            }
        });

        loadResources(); // Carrega os recursos ao iniciar
    }
});



// Funções para Requests
function loadRequests() {
    const list = document.getElementById('requestsList');
    if (!list) return;

    fetchWithAuth(`${API_URL}/requests/`)
    .then(response => {
        if (response.status === 403) {
            alert('Acesso negado.');
            window.location.href = '/frontend/index.html';
            return Promise.reject('Acesso negado');
        }
        if (!response.ok) {
            throw new Error('Erro ao carregar solicitações');
        }
        return response.json();
    })
    .then(requests => {
        list.innerHTML = '';
        requests.forEach(req => {
            const li = document.createElement('li');
            li.innerHTML = `
                <div class="resource-line"><strong>Equipamento solicitado:</strong> ${req.equipment_name}</div>
                <div class="resource-line"><strong>Status:</strong> ${req.status}</div>
            `;

            if (req.status === 'Pendente') {
                // Botão Concluir
                const btnConcluir = document.createElement('button');
                btnConcluir.textContent = 'Concluir';
                btnConcluir.className = 'logar';

                // Container para input e botão salvar (inicialmente oculto)
                const inputContainer = document.createElement('div');
                inputContainer.style.marginTop = '8px';
                inputContainer.style.display = 'none';

                const inputQuantity = document.createElement('input');
                inputQuantity.type = 'number';
                inputQuantity.min = '1';
                inputQuantity.placeholder = 'Quantidade';
                inputQuantity.style.marginRight = '8px';

                const btnSalvar = document.createElement('button');
                btnSalvar.textContent = 'Salvar';
                btnSalvar.className = 'logar';

                inputContainer.appendChild(inputQuantity);
                inputContainer.appendChild(btnSalvar);

                btnConcluir.onclick = () => {
                    btnConcluir.style.display = 'none';
                    inputContainer.style.display = 'block';
                    inputQuantity.focus();
                };

                btnSalvar.onclick = () => {
                    const quantity = inputQuantity.value;
                    if (!quantity || quantity <= 0) {
                        alert('Por favor, insira uma quantidade válida.');
                        inputQuantity.focus();
                        return;
                    }

                    fetchWithAuth(`${API_URL}/requests/${req.id}`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ 
                            status: 'Concluído',
                            quantity: Number(quantity)
                        })
                    })
                    .then(response => {
                        if (response.status === 403) {
                            alert('Acesso negado.');
                            window.location.href = '/frontend/index.html';
                            return Promise.reject('Acesso negado');
                        }
                        if (!response.ok) {
                            throw new Error('Erro ao atualizar solicitação');
                        }
                        return response.json();
                    })
                    .then(() => loadRequests())
                    .catch(error => {
                        console.error('Erro ao atualizar solicitação:', error);
                        alert('Erro ao atualizar solicitação');
                    });
                };

                li.appendChild(btnConcluir);
                li.appendChild(inputContainer);
            }

            list.appendChild(li);
        });
    })
    .catch(error => {
        console.error('Erro ao carregar solicitações:', error);
        list.innerHTML = '<li>Erro ao carregar solicitações</li>';
    });
}

if (document.getElementById('requestForm')) {
    document.getElementById('requestForm').addEventListener('submit', event => {
        event.preventDefault();
        const request = {
            equipment_name: document.getElementById('equipment_name').value
        };
        fetchWithAuth(`${API_URL}/request_resources/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(request)
        })
        .then(response => {
            if (response.status === 403) {
                alert('Acesso negado. Apenas gerentes ou administradores podem criar solicitações.');
                window.location.href = '/frontend/index.html';
                return Promise.reject('Acesso negado');
            }
            if (!response.ok) {
                throw new Error('Erro ao criar solicitação');
            }
            return response.json();
        })
        .then(() => loadRequests())
        .catch(error => {
            console.error('Erro ao criar solicitação:', error);
            alert('Erro ao criar solicitação');
        });
    });
}

// Funções para Alerts
function loadAlerts() {
    const alertContainer = document.getElementById('alert-container');
    const alertLocation = document.getElementById('alert-location');
    const alertVillain = document.getElementById('alert-villain');
    const alertType = document.getElementById('alert-type');
    const siren = document.getElementById('siren');

    if (!alertContainer || !alertLocation || !alertVillain || !alertType || !siren) {
        console.error('Elementos do alerta não encontrados');
        return;
    }

    fetchWithAuth(`${API_URL}/alerts/`)
        .then(response => {
            if (response.status === 403) {
                alert('Acesso negado. Apenas administradores podem visualizar alertas.');
                window.location.href = '/frontend/index.html';
                return Promise.reject('Acesso negado');
            }
            if (!response.ok) {
                throw new Error('Erro ao carregar alertas');
            }
            return response.json();
        })
        .then(alerts => {
            if (!alerts || alerts.length === 0) {
                alertContainer.innerHTML = '<p>Nenhum alerta disponível.</p>';
                return;
            }

            let currentAlertIndex = 0;

            function showNextAlert() {
                if (currentAlertIndex >= alerts.length) {
                    currentAlertIndex = 0; // Volta ao início para looping
                }

                const alert = alerts[currentAlertIndex];
                alertLocation.textContent = alert.location;
                alertVillain.textContent = alert.villain;
                alertType.textContent = alert.type;

                alertContainer.classList.add('blink');
                siren.currentTime = 0;
                siren.play().catch(e => console.error('Erro ao tocar sirene:', e));

                setTimeout(() => {
                    alertContainer.classList.remove('blink');
                }, 15000);

                currentAlertIndex++;
                setTimeout(showNextAlert,60000);
            }

            setTimeout(showNextAlert, 5000);
        })
        .catch(error => {
            console.error('Erro ao carregar alertas:', error);
            alertContainer.innerHTML = '<p>Erro ao carregar alertas.</p>';
        });
}

// Funções para Dashboard
function fetchStatsAndRenderCharts() {
    const ctx1 = document.getElementById('crimesChart');
    const ctx2 = document.getElementById('neighborhoodsChart');
    if (!ctx1 || !ctx2) return;

    fetchWithAuth(`${API_URL}/dashboard/stats`)
    .then(response => {
        if (response.status === 403) {
            alert('Acesso negado.');
            window.location.href = '/frontend/index.html';
            return Promise.reject('Acesso negado');
        }
        if (!response.ok) {
            throw new Error('Erro ao carregar estatísticas');
        }
        return response.json();
    })
    .then(stats => {
        // Destroi os gráficos existentes (se houver)
        if (crimesChartInstance) {
            crimesChartInstance.destroy();
        }
        if (neighborhoodsChartInstance) {
            neighborhoodsChartInstance.destroy();
        }

        // Gráfico de crimes por vilão
        const villains = {};
        stats.forEach(stat => {
            villains[stat.villain] = (villains[stat.villain] || 0) + stat.crimes;
        });
        crimesChartInstance = new Chart(ctx1.getContext('2d'), {
            type: 'bar',
            data: {
                labels: Object.keys(villains),
                datasets: [{
                    label: 'Crimes por Vilão',
                    data: Object.values(villains),
                    backgroundColor: '#FFD700'
                }]
            },
            options: { scales: { y: { beginAtZero: true } } }
        });

        // Gráfico de bairros perigosos
        const neighborhoods = {};
        stats.forEach(stat => {
            neighborhoods[stat.neighborhood] = (neighborhoods[stat.neighborhood] || 0) + stat.crimes;
        });
        neighborhoodsChartInstance = new Chart(ctx2.getContext('2d'), {
            type: 'pie',
            data: {
                labels: Object.keys(neighborhoods),
                datasets: [{
                    data: Object.values(neighborhoods),
                    backgroundColor: ['#7c6a03ff', '#7c7b7bff', '#000000', '#FFD700', '#333333', '#b99621ff']
                }]
            }
        });
    })
    .catch(error => {
        console.error('Erro ao carregar estatísticas:', error);
        alert('Erro ao carregar estatísticas');
    });
}


// Inicialização dinâmica
document.addEventListener('DOMContentLoaded', () => {
    renderMenu();
    if (window.location.pathname.includes('welcome.html')) {
        renderWelcomeMessage();
    }
    if (document.getElementById('loginForm')) {
        document.getElementById('loginForm').addEventListener('submit', login);
    }
    if (window.location.pathname.includes('users.html')) {
        loadUsers();
    }
    if (window.location.pathname.includes('resources.html')) {
        loadResources();
    }
    if (window.location.pathname.includes('request.html')) {
        loadRequests();
    }
    if (window.location.pathname.includes('request_resource.html')) { // Corrigido de 'request_resourse.html'
        loadRequests();
    }
    if (window.location.pathname.includes('dashboard.html')) {
        fetchStatsAndRenderCharts();
    }
    if (window.location.pathname.includes('alerts.html')) {
        loadAlerts();
    }
});