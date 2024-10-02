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
    const records = await pb.collection('Requests').getFullList({sort: '-created' });
    //const fieldsToKeep = ['state', 'pseudonym', 'birth', 'sex', 'gender', 'email', 'phone', 'phone_app', 'phone_extra', 'phone_extra_app', 'address_cep', 'address_state', 'address_city', 'address_neighborhood', 'address_location', 'address_number', 'address_extra', 'reason', 'religion', 'psychotherapy', 'psychiatry', 'spiritual_treatment', 'illnesses', 'symptoms', 'medicines', 'treatments', 'allergies' ];
    const fieldsToKeep = ['state', 'pseudonym', 'gender', 'email', 'phone', 'phone_app', 'reason'];
    const filteredRecords = records.map(record => {
        const filteredRecord = {};
        fieldsToKeep.forEach(field => {
            if (record[field] !== undefined) {
                filteredRecord[field] = record[field];
            }
        });
        return filteredRecord;
    });
    const component = document.getElementById('requests');
    const headerComponent = document.getElementById('table-header');
    if (filteredRecords.length === 0) {
        component.innerHTML = '<tr><td colspan="100%" class="text-center">Nenhum registro encontrado.</td></tr>';
        return;
    }
    const keys = Object.keys(filteredRecords[0]);
    keys.forEach(key => {
        const th = document.createElement('th');
        th.innerText = key.charAt(0).toUpperCase() + key.slice(1); 
        headerComponent.appendChild(th);
    });
    filteredRecords.forEach(record => {
        const tr = document.createElement('tr');
        keys.forEach(key => {
            const td = document.createElement('td');
            td.innerText = record[key] || 'N/A'; 
            tr.appendChild(td);
        });
        component.appendChild(tr);
    }); 
}