// Icone | Tipo | Valor | Estado (Inconclusivo, Certo, Errado, Desativado)

let forms = [
	    [["text", "user", "Nome completo", "", 0], ["text", "user", "Nome social", "", 0], ["date", "calendar", "Data de Nascimento", new Date(), 0], ["dropdown", "user", "Sexo", "", 0], ["dropdown", "user", "Gênero", "", 0]],
        [["email", "at-sign", "E-mail", "", 0], ["text", "phone", "Telefone", "", 0], ["dropdown", "star", "Aplicativos", 0], ["text", "phone", "Telefone Emergencial", "", 0], ["dropdown", "star", "Aplicativos", 0]],
	    [["text", "map", "CEP", "", 0], ["text", "map", "Estado", "", 0], ["text", "map", "Cidade", "", 0], ["text", "map", "Bairro", "", 0], ["text", "map-pin", "Logradouro", "", 0], ["text", "map-pin", "Número", "", 0], ["text", "map-pin", "Complemento", "", 0]],
        [["text", "smile", "Qual é o motivo da solicitação?", "", 0], ["dropdown", "tablet", "Religião", "", 0]],
        [["dropdown", "tablet", "Estou fazendo algum tratamento médico", 0],["text", "tablet", "Quais?", "", 0],["dropdown", "tablet", "Faço uso de medicamentos", 0],["text", "tablet", "Quais?", "", 0],["dropdown", "tablet", "Eu desmaio sem causa aparente", 0],["dropdown", "tablet", "Eu vejo vultos", 0],["dropdown", "tablet", "Eu escuto vozes", 0],["dropdown", "tablet", "Tenho pensamentos negativos / suicidas", 0],["dropdown", "tablet", "Perdi um membro da família recentemente", 0],["dropdown", "tablet", "Eu tenho alergias", 0],["text", "tablet", "Quais?", "", 0],["dropdown", "tablet", "Faço psicoterapia", 0],["dropdown", "tablet", "Fiz / Faço tratamento psiquiátrico", 0],["dropdown", "tablet", "Eu já fiz tratamento espiritual", 0]],
        [["dropdown", "smile", "Ciente", 0]],
];

const dropdownValues = [["Masculino", "Feminino", "Outro", "Prefiro Não Informar"], ["Homem", "Mulher", "Outro", "Prefiro Não Informar"], ["Whatsapp", "Telegram", "Ambos", "Nenhum"], ["Catolicismo", "Budismo", "Ateísmo", "Outro"], ["Sim", "Não", "Prefiro Não Informar"], ["Sim", "Não"]];

let pageIndex = 0;

document.addEventListener("DOMContentLoaded", () => {
	buildForms(pageIndex);
});

function changeValue(pindex, index, value, type) {
	forms[pindex][index][3] = value;
	let passed = false;

	switch (type) {
        case "text": passed = true; break; //case "text": passed = value.length > 3 ? true : false; break;
        case "dropdown": passed = value == "" ? false : true; break;
        case "date":
            const currentDate = new Date();
            const inputDate = new Date(value);
            const minDate = new Date();
            minDate.setFullYear(currentDate.getFullYear() - 150);
            if (inputDate < currentDate && inputDate > minDate) passed = true;
            break;
		case "email":
			const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
			passed = emailRegex.test(value);
			break;
	}

	const element = document.getElementById(`input-${pindex}-${index}`);
	if (!element) return;

	if (passed == true) {
		element.classList.add("success");
		element.classList.remove("error");
		forms[pindex][index][4] = 2;
	} else {
        showErrorBubble("Um campo não foi preenchido corretamente!");
		element.classList.add("error");
		element.classList.remove("success");
		forms[pindex][index][4] = 1;
	}
}

function buildContent(index){
    let html = '';

    switch(index){
        case 0: html = `<h2 class="mb-5">Dados Pessoais</h2>`; break;
        case 1: html = `<h2 class="mb-5">Meios de Contato</h2>`; break;
        case 2: html = `<h2 class="mb-5">Endereço</h2>`; break;
        case 3: html = `<h2 class="mb-5">Dados Extras</h2>`; break;
        case 4: html = `<h2 class="mb-5">Sintomas</h2>`; break;
        case 5: html = `<h2 class="mb-5">Termos de Uso</h2> <h4>EU ESTOU CIENTE SOBRE A OBRIGATORIEDADE DE ASSISTIR ÀS DOUTRINÁRIAS, ÀS QUARTAS FEIRAS, ÀS 19:00, PRESENCIALMENTE, NA RUA ALAGOAS, 121-MARIA PRETA - SAJ-BA, OU ON-LINE, ATRAVÉS DO CANAL SER - SOCIEDADE ESPÍRITA RAFAEL LÍRIO, NO YOUTUBE.</h4>`; break;
    }

    return html;
}

function getDropdownValues(pindex, index) {
    let html = '';
    if(pindex == 0){
        if(index == 3) {
            html += `<option value="", 0>${forms[pindex][index][2]}</option>`;
            for(let i = 0; i < dropdownValues[0].length; i++){
                html += `<option value="option${i}">${dropdownValues[0][i]}</option>'`;
            }
        } else if (index == 4) {
            html += `<option value="", 0>${forms[pindex][index][2]}</option>`;
            for(let i = 0; i < dropdownValues[1].length; i++){
                html += `<option value="option${i}">${dropdownValues[1][i]}</option>'`;
            }
        }
    }
    if(pindex == 1) {
        html += `<option value="", 0>${forms[pindex][index][2]}</option>`;
        for(let i = 0; i < dropdownValues[2].length; i++){
            html += `<option value="option${i}">${dropdownValues[2][i]}</option>'`;
        }
    }
    if(pindex == 3) {
        html += `<option value="", 0>${forms[pindex][index][2]}</option>`;
        for(let i = 0; i < dropdownValues[3].length; i++){
            html += `<option value="option${i}">${dropdownValues[3][i]}</option>'`;
        }
    }
    if(pindex == 4) {
        html += `<option value="", 0>${forms[pindex][index][2]}</option>`;
        for(let i = 0; i < dropdownValues[4].length; i++){
            html += `<option value="option${i}">${dropdownValues[4][i]}</option>'`;
        }
    }
    if (pindex == 5) {
        html += `<option value="", 0>${forms[pindex][index][2]}</option>`;
        for(let i = 0; i < dropdownValues[5].length; i++){
            html += `<option value="option${i}">${dropdownValues[5][i]}</option>'`;
        }
    }
    return html;
}

function buildInput(type, icon, placeholder, value, flag, pindex, index) {
	let html = "";
    switch(type){
        case "text": html += `<div class="col-md-6 col-12"> <div id="input-${pindex}-${index}" class="form-area d-flex align-items-center mb-3 px-3"> <i data-feather="${icon}" class="me-3"></i> <input class="input fit-w" type="${type}" value="${value}" placeholder="${placeholder}" onchange="changeValue(${pindex}, ${index}, this.value, '${type}')"/> </div> </div>`; break;
        case "dropdown": html += `<div class="col-md-6 col-12"> <div id="input-${pindex}-${index}" class="form-area d-flex align-items-center mb-3 px-3"> <i data-feather="${icon}" class="me-3"></i> <select class="input fit-w" onchange="changeValue(${pindex}, ${index}, this.value, '${type}')">${getDropdownValues(pindex, index)}</select></div> </div>`; break;
        case "date": html += `<div class="col-md-6 col-12"> <div id="input-${pindex}-${index}" class="form-area d-flex align-items-center mb-3 px-3"> <i data-feather="${icon}" class="me-3"></i> <input class="input fit-w" type="${type}" value="${value}" placeholder="${placeholder}" onchange="changeValue(${pindex}, ${index}, this.value, '${type}')"/> </div> </div>`; break;
        case "email": html += `<div class="col-md-6 col-12"> <div id="input-${pindex}-${index}" class="form-area d-flex align-items-center mb-3 px-3"> <i data-feather="${icon}" class="me-3"></i> <input class="input fit-w" type="${type}" value="${value}" placeholder="${placeholder}" onchange="changeValue(${pindex}, ${index}, this.value, '${type}')"/> </div> </div> <div></div>`; break;
    }
	return html;
}

function buildForms(index) {
    const element = document.getElementById("forms");
	if (index == "+") index = pageIndex + 1;
	if (index == "-") index = pageIndex - 1;
	const formData = forms[index];
	let content = "";

	if (!formData) return;

	const currentStepElement = document.getElementById(`step_${pageIndex}`);
	currentStepElement.classList.remove("selected");
	const targetStepElement = document.getElementById(`step_${index}`);
	targetStepElement.classList.add("selected");

	pageIndex = index;
	content += buildContent(index) + `<div class="row fit-w m-0">`;

	formData.forEach((data, index) => {
        const [type, icon, placeholder, value, flag] = data;
        content += buildInput(type, icon, placeholder, value, flag, pageIndex, index);
	});

	content += `</div> <div class="line my-5"></div> <div class="row mt-4">`;
    content += `<div class="${pageIndex == 0? "d-none" : pageIndex == 5? "col-12" : "col-md-6 col-12 mb-md-0 mb-3"}">  <div class="button secondary d-flex align-items-center justify-content-center fit-w" onclick="buildForms('-')"><h4 class="me-3">Voltar</h4><i data-feather="chevron-left"></i></div>  </div>`;
    content += `<div class="${pageIndex == 5? "d-none" : pageIndex == 0? "col-12" : "col-md-6 col-12"}">  <div class="button d-flex align-items-center justify-content-center fit-w" onclick="buildForms('+')"><h4 class="me-3">Continuar</h4><i data-feather="chevron-right"></i></div>  </div>`;
    content += `</div>`

	element.innerHTML = content;
	feather.replace();
}

timer = 0;

function showErrorBubble(string) {
    const bubble = document.getElementById('errorBubble');

    bubble.style.left = `auto`;
    bubble.style.bottom = `90%`;
    bubble.innerHTML = `<h4><strong>Hey!</strong> ${string}</h4>`;
    bubble.style.display = 'block'

    setTimeout(() => {
        if(timer <= 0) hideErrorBubble()
    }, 1000 * 5)

    timer = 5;
}

function hideErrorBubble() {
    document.getElementById('errorBubble').style.display = 'none';
}

setInterval(() => {
    timer -= 1;
}, 1000)