function loadrequestconcluido() {
    const list = document.getElementById('requestListConcluido');
    if (!list) return;

    fetchWithAuth(`${API_URL}/requests/`)
    .then(response=>{
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
        requests.filter(request => request.status === 'Concluido')
        .forEach(request => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `
                <strong>Equipamento solicitado:</strong> ${request.equipment_name} <br>
                <strong>Status:</strong> ${request.status} <br>
                <strong>Quantidade:</strong> ${request.quantity} <br>
            `;
            list.appendChild(listItem);
        });
    })
    .catch(error => {
        console.error('Erro ao carregar solicitações:', error);
        list.innerHTML = '<li>Erro ao carregar solicitações</li>';
    });
}