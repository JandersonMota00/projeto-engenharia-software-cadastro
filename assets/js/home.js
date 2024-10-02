const pb = new PocketBase('https://atendimento-fraterno.pockethost.io');

let records = null;
let values = {};
let filters = ['', '', ''];
let role = '';
let currentKey = null;
let popupTimer = 0;

function main() {
    setInterval(()=> {
        popupTimer -= 3;
        if(popupTimer <= 0) hidePopup()
    }, 3000);
}

async function changeValue(component) {
    const key = component.id.slice(6);
    let value = component.value;
    values[key] = value;
    console.log(values);
}

function changeFilter(component) {
    const type = component.id.slice(7);
    console.log(type);
    const index = type == 'state' ? 0 : type == 'gender' ? 1 : 2;
    console.log(index);
    filters[index] = component.value;
    loadRequests();
}

async function saltedHashSHA256(value) {
    const encoder = new TextEncoder();
    const data = encoder.encode("S" + value);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(byte => byte.toString(16).padStart(2, '0')).join('');
    return hashHex;
}

async function login() {
    const login = await saltedHashSHA256(values.login);
    const password = await saltedHashSHA256(values.password);
    console.log(`login: ${login}\npassword: ${password}`);
    const authData = await pb.collection('Staff').authWithPassword(login, password).catch(() => {});
    if(!pb.authStore.isValid) {
        showPopup('Informações de Login inválidas!', document.getElementById('input-login'))
        return;
    }
    document.getElementById('loginScreen').classList.add('d-none');
    document.getElementById('homeScreen').classList.remove('d-none');
    role = capitalizeFirstLetter(pb.authStore.model.role);
    document.getElementById('role-text').innerHTML = role;
    loadRequests();
}

async function logout() {
    await pb.authStore.clear();
    document.getElementById('loginScreen').classList.remove('d-none');
    document.getElementById('homeScreen').classList.add('d-none');
}

function capitalizeFirstLetter(string) {
    if (!string) return '';
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function onTableClick(id) {
    console.log(id);
    const record = records.find(record => record.id == id);
    if(!record) return;
    console.log(record);

    const fieldsToKeep = ['state', 'pseudonym', 'sex', 'gender', 'email', 'phone', 'phone_app', 'phone_extra', 'phone_extra_app', 'address_state', 'address_city', 'address_neighborhood', 'address_location', 'address_number', 'reason', 'religion', 'psychotherapy', 'psychiatry', 'spiritual_treatment', 'illnesses', 'symptoms', 'medicines', 'treatments', 'allergies', "faint", "shadows", "voices", "suicide", "death"];
    const filteredRecord = {}; 
    fieldsToKeep.forEach(field => {
        if (record.hasOwnProperty(field)) {
            filteredRecord[field] = record[field];
        }
    });

    const component = document.getElementById('custom-request');
    const headerComponent = document.getElementById('custom-table-header');
    component.innerHTML = '';
    headerComponent.innerHTML = '';
    const keys = Object.keys(filteredRecord);
    keys.forEach(key => {
        if(key == 'id') return;
        const th = document.createElement('th');
        th.scope = "col";
        let text = '';
        switch(key) {
            case 'state': text = "Estado"; break;
            case 'pseudonym': text = "Pseudônimo"; break;
            case 'sex': text = "Sexo"; break;
            case 'gender': text = "Gênero"; break;
            case 'email': text = "E-mail"; break;
            case 'phone': text = "Telefone"; break;
            case 'phone_app': text = "Aplicativo"; break;
            case 'phone_extra': text = "Telefone Extra"; break;
            case 'phone_extra_app': text = "Aplicativo Extra"; break;
            case 'address_state': text = "Estado do Endereço"; break;
            case 'address_city': text = "Cidade do Endereço"; break;
            case 'address_neighborhood': text = "Bairro do Endereço"; break;
            case 'address_location': text = "Localização do Endereço"; break;
            case 'address_number': text = "Número do Endereço"; break;
            case 'reason': text = "Motivo"; break;
            case 'religion': text = "Religião"; break;
            case 'psychotherapy': text = "Fez Psicoterapia?"; break;
            case 'psychiatry': text = "Fez Psiquiatria?"; break;
            case 'spiritual_treatment': text = "Fez Tratamento Espiritual?"; break;
            case 'illnesses': text = "Doenças"; break;
            case 'symptoms': text = "Sintomas"; break;
            case 'medicines': text = "Medicamentos"; break;
            case 'treatments': text = "Tratamentos"; break;
            case 'allergies': text = "Alergias"; break;
            case 'faint': text = "Desmaios"; break;
            case 'shadows': text = "Vê vultos"; break;
            case 'voices': text = "Escuta vozes"; break;
            case 'suicide': text = "Pensamentos Negativos"; break;
            case 'death': text = "Entes faleceram"; break;
        }
        th.innerText = text || key;
        headerComponent.appendChild(th);
    });
    const tr = document.createElement('tr');
    keys.forEach(key => {
        const td = document.createElement('td');
        td.innerText = filteredRecord[key] || 'Vazio'; 
        if(td.innerText == "true") td.innerText = 'Sim';
        if(td.innerText == "false") td.innerText = 'Não';
        tr.appendChild(td);
    });
    component.appendChild(tr);
    $("#custom-table").modal('show');
}

function loadGraphs() {
    if(role != 'Diretor') return;
    document.getElementById('graph-zone').classList.remove('d-none');
    let stateData = { Aguardando: 0, Análise: 0, Concluído: 0 };
    let genderData = { Homem: 0, Mulher: 0, Outro: 0, Segredo: 0 };
    let colors1 = ['#1582c5', '#D5E0E9', '#00a3d4'];
    let colors2 = ['#00a3d4', '#96abbd', '#1582c5', '#D5E0E9'];

    records.forEach(record => {
        if (stateData[record.state] !== undefined) {
          stateData[record.state]++;
        }
        if (genderData[record.gender] !== undefined) {
          genderData[record.gender]++;
        }
    });

    let statePieData = Object.keys(stateData).map(key => ({ name: key, value: stateData[key] }));
    let genderPieData = Object.keys(genderData).map(key => ({ name: key, value: genderData[key] }));

    var stateChart = echarts.init(document.getElementById('graph-state'));
    var stateOption = {
        title: { text: 'Distribuição por Estado', left: 'center' },
        color: colors1,
        tooltip: { trigger: 'item' },
        series: [{
            name: 'Estado da Consulta',
            type: 'pie',
            radius: '50%',
            minAngle: 36,
            data: statePieData,
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }]
    };
    stateChart.setOption(stateOption);

    var genderChart = echarts.init(document.getElementById('graph-gender'));
    var genderOption = {
        title: { text: 'Distribuição por Gênero', left: 'center' },
        color: colors2,
        tooltip: { trigger: 'item' },
        series: [{
            name: 'Gênero',
            type: 'pie',
            radius: '50%',
            minAngle: 36,
            data: genderPieData,
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }]
    };
    genderChart.setOption(genderOption);
}

async function changeState(component) {
    if(!component.value) return;
    let record = records.find(record => record.id = currentKey);
    if(!record) return;
    record.state = component.value;
    const putRecord = await pb.collection('Requests').update(record.id, record);
    if(!putRecord) return;
    $("#custom-table").modal('hide');
    loadRequests();
}

async function loadRequests() {
    const component = document.getElementById('requests');
    const headerComponent = document.getElementById('table-header');
    component.innerHTML = '';
    headerComponent.innerHTML = '';
    records = await pb.collection('Requests').getFullList({sort: 'created' });
    //const fieldsToKeep = ['state', 'pseudonym', 'birth', 'sex', 'gender', 'email', 'phone', 'phone_app', 'phone_extra', 'phone_extra_app', 'address_cep', 'address_state', 'address_city', 'address_neighborhood', 'address_location', 'address_number', 'address_extra', 'reason', 'religion', 'psychotherapy', 'psychiatry', 'spiritual_treatment', 'illnesses', 'symptoms', 'medicines', 'treatments', 'allergies' ];
    const fieldsToKeep = ['state', 'pseudonym', 'gender', 'email', 'phone', 'phone_app', 'id'];
    const filteredRecords = records.map(record => {
        const filteredRecord = {};
        fieldsToKeep.forEach(field => {
            if (record[field] !== undefined) {
                filteredRecord[field] = record[field];
            }
        });
        return filteredRecord;
    });
    if (filteredRecords.length === 0) {
        component.innerHTML = '<tr><td colspan="100%" class="text-center">Nenhum registro encontrado.</td></tr>';
        return;
    }
    const keys = Object.keys(filteredRecords[0]);
    keys.forEach(key => {
        if(key == 'id') return;
        const th = document.createElement('th');
        th.scope = "col";
        let text = '';
        switch(key) {
            case 'state': text = "Estado"; break;
            case 'pseudonym': text = "Pseudônimo"; break;
            case 'gender': text = "Gênero"; break;
            case 'email': text = "E-mail"; break;
            case 'phone': text = "Telefone"; break;
            case 'phone_app': text = "Aplicativo"; break;
            case "id": text = "Código"; break;
        }
        th.innerText = text;
        headerComponent.appendChild(th);
    });
    filteredRecords.forEach(record => {
        if(!(record.state.includes(filters[0]))) return;
        if(!(record.gender.includes(filters[1]))) return;
        if(!(record.phone_app.includes(filters[2]))) return;
        const tr = document.createElement('tr');
        keys.forEach(key => {
            if(key == "id") {
                currentKey = record[key];
                tr.onclick = function() { onTableClick(record[key]) };
                return;
            }
            const td = document.createElement('td');
            td.innerText = record[key] || 'N/A'; 
            if(key == "state") {
                let color = '';
                switch(record[key]){
                    case "Aguardando": color = '#128f3a'; break;
                    case "Análise": color = '#FFC43D'; break;
                    case "Concluído": color = '#1582c5'; break;
                }
                td.style.backgroundColor = color;
            }
            tr.appendChild(td);
        });
        component.appendChild(tr);
    }); 
    loadGraphs();
}

function showPopup(string, element) {
    const popup = document.getElementById('popup');
    const rect = element.getBoundingClientRect();
    popup.style.left = `${rect.left + window.scrollX}px`;
    popup.style.top = `${rect.top + window.scrollY - 100}px`;
    popup.innerHTML = `<h4>${string}</h4>`;
    popup.style.display = 'block'
    popup.style.backgroundColor = '#231f20';
    popupTimer = 5;
}

function hidePopup() {
    document.getElementById('popup').style.display = 'none';
}

main();