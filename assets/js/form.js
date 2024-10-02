const pb = new PocketBase('https://atendimento-fraterno.pockethost.io');

let pageIndex = 0;
let popupTimer = 0;
let agreed = false;

let values = {};

let requirements = ['faint', 'shadows', 'voices', 'suicide', 'death'];

function main() {
    setInterval(()=> {
        popupTimer -= 3;
        if(popupTimer <= 0) hidePopup()
    }, 3000);
}

async function conclude(){
    if(!agreed) {
        showPopup("Você precisa concordar com os nossos termos!", document.getElementById('input-terms'));
        return;
    }

    let gate = true;
    requirements.forEach(requirement => {
        if(!(values[requirement] === true || values[requirement] === false)) gate = false;
    });

    if(gate) {
        values.state = "Aguardando";
        values.created_date = new Date();
        const json = JSON.stringify(values);
        const record = await pb.collection('Requests').create(json).catch((error) => {});
        if(!record) gate = false;
    }

    if(!gate) {
        showPopup("Algum dos campos obrigatórios não foi preenchido corretamente!", document.getElementById('input-terms'));
        return;
    }
    $('#conclusion').modal('show');
}

async function changePage(type) {
    let stepElement = document.getElementById(`step_${pageIndex}`);
    let pageElement = document.getElementById(`page_${pageIndex}`);
	stepElement.classList.remove("selected");
    pageElement.classList.add("d-none");
    if (type == "+") pageIndex++;
	else if (type == "-") pageIndex--;
    else pageIndex = type;
    stepElement = document.getElementById(`step_${pageIndex}`);
    pageElement = document.getElementById(`page_${pageIndex}`);
	stepElement.classList.add("selected");
    pageElement.classList.remove("d-none");

}

async function changeValue(component) {
    let completed = 1;
    const key = component.id.slice(6);
    let value = component.value;

    if(value == "true") value = true;
    if(value == "false") value = false;

    switch(key) {
        case "terms": agreed = value; return;
        case 'name': value = sanitizeText(value, "name"); break;
        case 'pseudonym': value = sanitizeText(value, "pseudonym"); break;
        case "email": completed = validateEmail(value); break; 
        case "address_cep": completed = await validateCep(value); break;
        case "phone": value = validatePhone(value, 'phone'); break; 
        case "phone_extra": value = validatePhone(value, 'phone_extra'); break; 
        case 'address_number': value = sanitizeNumber(value, 'address_number'); break;
    }

    if(completed == 0) {
        return;
    }
    
    switch(key){
        case "cep": values[key] = completed; break;
        default: values[key] = value; break;
    }
}

function sanitizeText(text, type) {
    const result = text.replace(/[^a-zA-ZÀ-ÿ\s]/g, '');
    document.getElementById(`input-${type}`).value = result;
    return result;
}

function sanitizeNumber(text, type) {
    const result = text.replace(/\D/g,'');
    document.getElementById(`input-${type}`).value = result;
    return result;
}

function validatePhone(number, type) {
    let phone = number;
    phone = phone.replace(/\D/g,'');
    const phoneWithDDDRegex = /^(\d{2})(\d{4,5})(\d{4})$/;
    const phoneWithoutDDDRegex = /^(\d{4,5})(\d{4})$/;
    if(phone.length == 11 && phoneWithDDDRegex.test(phone)) phone = phone.replace(phoneWithDDDRegex,'($1) $2-$3');
    else if(phone.length == 10 && phoneWithDDDRegex.test(phone)) phone = phone.replace(phoneWithDDDRegex,'($1) $2-$3');
    else if(phoneWithoutDDDRegex.test(phone)) phone = phone.replace(phoneWithoutDDDRegex,'$1-$2');
    document.getElementById(`input-${type}`).value = phone;
    return phone;
}

async function validateCep(cep) {
    let value = cep.replace(/\D/g, '');
    if (value.length === 8) {
        value = value.replace(/(\d{5})(\d{3})/, '$1-$2'); 
        document.getElementById('input-address_cep').value = value;
        values.address_cep = value;
        const response = await fetch(`https://viacep.com.br/ws/${value}/json/`);
        if(!response.ok) return 0;
        const data = await response.json();
        if(!data.estado) return 0;
        document.getElementById('input-address_state').value = data.estado;
        values.address_state = data.estado;
        document.getElementById('input-address_city').value = data.localidade;
        values.address_city = data.localidade;
        document.getElementById('input-address_neighborhood').value = data.bairro;
        values.address_neighborhood = data.bairro;
        document.getElementById('input-address_location').value = data.logradouro;
        values.address_location = data.logradouro;
    }
    document.getElementById('input-address_cep').value = value;
    return value;
}

function validateEmail(email) {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    const result = emailRegex.test(email) === true? 1 : 0;
    return result;
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