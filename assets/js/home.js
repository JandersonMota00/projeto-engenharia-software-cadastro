const pb = new PocketBase('https://atendimento-fraterno.pockethost.io');

let values = {};

async function changeValue(component) {
    const key = component.id.slice(6);
    let value = component.value;
    values[key] = value;
    console.log(values);
}

async function login() {
    const authData = await pb.collection('Staff').authWithPassword(values.login, values.password);
    if(!pb.authStore.isValid) return;
    document.getElementById('loginScreen').classList.add('d-none');
    document.getElementById('homeScreen').classList.remove('d-none');
    loadRequests();
}

async function logout() {
    await pb.authStore.clear();
    document.getElementById('loginScreen').classList.remove('d-none');
    document.getElementById('homeScreen').classList.add('d-none');
}

async function loadRequests() {
    const records = await pb.collection('Requests').getFullList({sort: '-created'});
    const component = document.getElementById('requests');
    const headerComponent = document.getElementById('table-header');
    if (records.length === 0) {
        component.innerHTML = '<tr><td colspan="100%" class="text-center">Nenhum registro encontrado.</td></tr>';
        return;
    }
    const keys = Object.keys(records[0]);
    keys.forEach(key => {
        const th = document.createElement('th');
        th.innerText = key.charAt(0).toUpperCase() + key.slice(1); 
        headerComponent.appendChild(th);
    });
    records.forEach(record => {
        const tr = document.createElement('tr');
        keys.forEach(key => {
            const td = document.createElement('td');
            td.innerText = record[key] || 'N/A'; 
            tr.appendChild(td);
        });
        component.appendChild(tr);
    }); 
}