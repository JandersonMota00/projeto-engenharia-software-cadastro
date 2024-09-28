const pb = new PocketBase('https://atendimento-fraterno.pockethost.io');

// TIPO | ICONE | PLACEHOLDER | VALOR | ESTADO

let forms = [
	    [["text", "user", "Nome completo", "", ""], ["text", "user", "Nome social", "", ""], ["date", "calendar", "Data de Nascimento", new Date(), ""], ["dropdown", "user", "Sexo", "", ""], ["dropdown", "user", "Gênero", "", ""]],
        [["email", "at-sign", "E-mail", "", ""], ["tel", "phone", "Telefone", "", ""], ["dropdown", "star", "Aplicativos", ""], ["tel", "phone", "Telefone Emergencial", "", ""], ["dropdown", "star", "Aplicativos", ""]],
	    [["text", "map", "CEP", "", ""], ["text", "map", "Estado", "", ""], ["text", "map", "Cidade", "", ""], ["text", "map", "Bairro", "", ""], ["text", "map-pin", "Logradouro", "", ""], ["text", "map-pin", "Número", "", ""], ["text", "map-pin", "Complemento", "", ""]],
        [["text", "smile", "Qual é o motivo da solicitação?", "", ""], ["dropdown", "tablet", "Religião", "", ""]],
        [["dropdown", "tablet", "Estou fazendo algum tratamento médico", ""],["text", "tablet", "Quais?", "", ""],["dropdown", "tablet", "Faço uso de medicamentos", ""],["text", "tablet", "Quais?", "", ""],["dropdown", "tablet", "Eu tenho alergias", ""],["text", "tablet", "Quais?", "", ""],["dropdown", "tablet", "Eu desmaio sem causa aparente", ""],["dropdown", "tablet", "Eu vejo vultos", ""],["dropdown", "tablet", "Eu escuto vozes", ""],["dropdown", "tablet", "Tenho pensamentos negativos / suicidas", ""],["dropdown", "tablet", "Perdi um membro da família recentemente", ""],["dropdown", "tablet", "Faço psicoterapia", ""],["dropdown", "tablet", "Fiz / Faço tratamento psiquiátrico", ""],["dropdown", "tablet", "Eu já fiz tratamento espiritual", ""]],
        [["dropdown", "smile", "Ciente", ""]],
];

//const dropdownValues = [["Masculino", "Feminino", "Intersexual", "Prefiro Não Informar"], ["Agênero", "Agênero", "Andrógino", "Apogênero", "Apôrêne", "Bigênero", "Demigênero", "Demimenina", "Demimenino", "Gênero Binário Feminino", "Gênero Binário Masculino", "Gênero Expandido", "Gênero Fluido", "Gênero Inconformista", "Gênero Nulo", "Gênero Queer", "Gênero Vago", "Homem Trans", "Intergênero", "Maverique", "Mulher Trans", "Neutrois", "Neutrois", "Não-binário", "Pangênero", "Poligênero", "Transgênero", "Transexual", "Travesti", "Outro", "Prefiro Não Informar"], ["Whatsapp", "Telegram", "Ambos", "Nenhum"], ["Agnosticismo", "Ateísmo", "Bahá'í", "Budismo", "Candomblé", "Catolicismo", "Confucionismo", "Cristianismo", "Espiritismo", "Hare Krishna", "Hinduísmo", "Islamismo", "Jainismo", "Judaísmo", "Mormonismo", "Ortodoxia Oriental", "Protestantismo", "Rastafarianismo", "Santo Daime", "Sikhismo", "Taoísmo", "Testemunhas de Jeová", "Umbanda", "Xintoísmo", "Zoroastrismo", "Outro"], ["Sim", "Não", "Prefiro Não Informar"], ["Sim", "Não"]];

const dropdownValues = [
    ["masculino", "feminino", "intersexual", "prefiro_nao_informar"],
    // Gêneros com grupos
    {
        "Gêneros Binários": ["masculino", "Feminino"],
        "Gêneros Não Binários": ["Não-binário", "Gênero Fluido", "Agênero", "Bigênero", "Demigênero", "Demimenino", "Demimenina", "Pangênero", "Andrógino", "Neutrois", "Intergênero", "Gênero Queer", "Poligênero", "Gênero Vago", "Gênero Inconformista", "Gênero Expandido", "Maverique", "Apôrêne"],
        "Identidades Transgêneras": ["Transgênero", "Homem Trans", "Mulher Trans", "Transexual", "Travesti"],
        "Identidades Sem Gênero": ["Agênero", "Neutrois", "Gênero Nulo", "Apogênero"]
    },
    ["Whatsapp", "Telegram", "Ambos", "Nenhum"], 
    [
        "Agnosticismo", "Ateísmo", "Bahá'í", "Budismo", "Candomblé", "Catolicismo",
        "Confucionismo", "Cristianismo", "Espiritismo", "Hare Krishna", "Hinduísmo", 
        "Islamismo", "Jainismo", "Judaísmo", "Mormonismo", "Ortodoxia Oriental", 
        "Protestantismo", "Rastafarianismo", "Santo Daime", "Sikhismo", "Taoísmo", 
        "Testemunhas de Jeová", "Umbanda", "Xintoísmo", "Zoroastrismo", "Outro"
    ], 
    ["Sim", "Não", "Prefiro Não Informar"], 
    ["Sim", "Não"]
];


let pageIndex = 0;


async function changeValue(pindex, index, value, type) {
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
        // FEITO POR JANDERSON
        case "tel":
            // Remove qualquer caractere que não seja número
            value = value.replace(/\D/g, '');

            // Limita o input a 11 dígitos
            if (value.length > 11) {
                value = value.slice(0, 11);
            }

            // Verifica se o campo de telefone está corretamente preenchido
            // Se for telefone fixo (10 dígitos) ou celular (11 dígitos), a validação passa
            passed = (value.length === 10 || value.length === 11);

            // Formata o telefone de acordo com o tamanho
            if (passed) {
                if (value.length === 11) {
                    // Formato para celular (XX) XXXXX-XXXX
                    value = value
                        .replace(/(\d{2})(\d)/, '($1) $2') // Adiciona os parênteses no DDD
                        .replace(/(\d{5})(\d)/, '$1-$2'); // Adiciona o hífen após os 5 primeiros números
                } else if (value.length === 10) {
                    // Formato para telefone fixo (XX) XXXX-XXXX
                    value = value
                        .replace(/(\d{2})(\d)/, '($1) $2') // Adiciona os parênteses no DDD
                        .replace(/(\d{4})(\d)/, '$1-$2'); // Adiciona o hífen após os 4 primeiros números
                }
            }

            forms[pindex][index][3] = value;
            break;
	}

	const element = document.getElementById(`input-${pindex}-${index}`);
	if (!element) return;

    if(pindex == 2) {
        if(index == 0) {
            if(value.length >= 9) value = value.replace(/[^0-9-]/g, '');
            
            if(value.length == 8) {
                value = value.replace(/(\d{5})(\d{3})/, '$1-$2');
                forms[pindex][index][3] = value;
            }

            if(forms[pindex][index][3].length == 9) {
                console.log(`Buscando por ${value}`);
                await fetch(`https://viacep.com.br/ws/${forms[pindex][index][3]}/json/`)
                .then(response => response.json())
                .then(data => {
                    element.querySelector('input').value = forms[pindex][index][3];
                    console.log(document.getElementById('input-2-1'));
                    document.getElementById('input-2-1').querySelector('input').value = data.uf;
                    forms[2][1][3] = data.uf;
                    document.getElementById('input-2-2').querySelector('input').value = data.localidade;
                    forms[2][2][3] = data.localidade;
                    document.getElementById('input-2-3').querySelector('input').value = data.bairro;
                    forms[2][3][3] = data.bairro;
                    document.getElementById('input-2-4').querySelector('input').value = data.logradouro;
                    forms[2][4][3] = data.logradouro;
                }).catch(() => {});
                passed = true;
            } else passed = false;
        }
    }

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
        case 5: html = `<h2 class="mb-5">Termos de Uso</h2> <div class="box p-4 mb-4"><h4 class="text-justify">Estou ciente da obrigatoriedade de participar das doutrinárias, que ocorrem às quartas-feiras, às 19:00. A participação pode ser presencial, na Rua Alagoas, 121 - Maria Preta, SAJ-BA, ou online através do canal SER - Sociedade Espírita Rafael Lírio no YouTube.</h4> </div>`; break;
    }

    return html;
}

function getDropdownValues(pindex, index) {
    let html = '';

    //FEITO POR JANDERSON
    if (pindex === 0 && index === 3) {
        // Campo de Sexo
        html += `<option value="" disabled selected>${forms[pindex][index][2]}</option>`;
        for (let i = 0; i < dropdownValues[0].length; i++) {
            html += `<option value="${dropdownValues[0][i]}">${dropdownValues[0][i]}</option>`;
        }
    } else if (pindex === 0 && index === 4) {
        // Campo de Gênero com Optgroups
        html += `<option value="" disabled selected>${forms[pindex][index][2]}</option>`;
        const genderGroups = dropdownValues[1];  // Grupos de Gêneros
        for (const group in genderGroups) {
            if (genderGroups.hasOwnProperty(group)) {
                html += `<optgroup label="${group}">`;
                for (let i = 0; i < genderGroups[group].length; i++) {
                    html += `<option value="${genderGroups[group][i]}">${genderGroups[group][i]}</option>`;
                }
                html += `</optgroup>`;
            }
        }
    } /*else if (pindex == 1 || pindex == 3 || pindex == 4 || pindex == 5) {
        // Outros campos de dropdown (sem optgroup)
        html += `<option value="" disabled selected>${forms[pindex][index][2]}</option>`;
        for (let i = 0; i < dropdownValues[pindex].length; i++) {
            html += `<option value="${dropdownValues[pindex][i]}">${dropdownValues[pindex][i]}</option>`;
        }
    }*/

    /*if(pindex == 0){
        if(index == 3) {
            html += `<option value="" disabled selected>${forms[pindex][index][2]}</option>`;
            for(let i = 0; i < dropdownValues[0].length; i++){
                html += `<option value="option${i}">${dropdownValues[0][i]}</option>`;
            }
        } else if (index == 4) {
            html += `<option value="" disabled selected>${forms[pindex][index][2]}</option>`;
            for(let i = 0; i < dropdownValues[1].length; i++){
                html += `<option value="option${i}">${dropdownValues[1][i]}</option>`;
            }
        }
    }*/
    if(pindex == 1) {
        html += `<option value="" disabled selected>${forms[pindex][index][2]}</option>`;
        for(let i = 0; i < dropdownValues[2].length; i++){
            html += `<option value="${dropdownValues[2][i]}">${dropdownValues[2][i]}</option>`;
        }
    }
    if(pindex == 3) {
        html += `<option value="" disabled selected>${forms[pindex][index][2]}</option>`;
        for(let i = 0; i < dropdownValues[3].length; i++){
            html += `<option value="${dropdownValues[3][i]}">${dropdownValues[3][i]}</option>`;
        }
    }
    if(pindex == 4) {
        html += `<option value="" disabled selected>${forms[pindex][index][2]}</option>`;
        for(let i = 0; i < dropdownValues[4].length; i++){
            html += `<option value="${dropdownValues[4][i]}">${dropdownValues[4][i]}</option>`;
        }
    }
    if (pindex == 5) {
        html += `<option value="" disabled selected>${forms[pindex][index][2]}</option>`;
        for(let i = 0; i < dropdownValues[5].length; i++){
            html += `<option value="${dropdownValues[5][i]}">${dropdownValues[5][i]}</option>`;
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
        // FEITO POR JANDERSON
        case "tel":
            html += `<div class="col-md-6 col-12"> 
                <div id="input-${pindex}-${index}" class="form-area d-flex align-items-center mb-3 px-3"> 
                    <i data-feather="${icon}" class="me-3"></i> 
                    <input class="input fit-w" type="${type}" value="${value}" placeholder="${placeholder}" onchange="changeValue(${pindex}, ${index}, this.value, '${type}')"/> 
                </div> 
            </div>`;
            setTimeout(() => formatPhoneInput(pindex, index), 0); // Chama a função para formatar o campo
            break;
        // Outros casos para outros tipos de inputs
        default:
            html += `<div class="col-md-6 col-12"> 
                <div id="input-${pindex}-${index}" class="form-area d-flex align-items-center mb-3 px-3"> 
                    <i data-feather="${icon}" class="me-3"></i> 
                    <input class="input fit-w" type="${type}" value="${value}" placeholder="${placeholder}" onchange="changeValue(${pindex}, ${index}, this.value, '${type}')"/> 
                </div> 
            </div>`;
    }
	return html;
}

function formatPhoneInput(pindex, index) {
    const inputElement = document.getElementById(`input-${pindex}-${index}`).querySelector('input');

    inputElement.addEventListener('input', function () {
        let value = inputElement.value;

        // Remove qualquer caractere que não seja número
        value = value.replace(/\D/g, '');

        // Verifica o terceiro dígito para determinar se é celular ou fixo
        const isCellPhone = value.length >= 3 && value[2] === '9';

        // Limita o input a 11 dígitos se for celular, e a 10 se for fixo
        if (isCellPhone) {
            value = value.slice(0, 11); // Celular tem até 11 dígitos
        } else {
            value = value.slice(0, 10); // Fixo tem até 10 dígitos
        }

        // Formata o telefone com DDD
        if (value.length > 0) {
            value = value.replace(/(\d{2})(\d)/, '($1) $2'); // Adiciona os parênteses no DDD
        }

        // Se for celular, formata como (XX) XXXXX-XXXX
        if (isCellPhone && value.length >= 10) {
            value = value.replace(/(\d{5})(\d)/, '$1-$2'); // Formata celular com 5 dígitos no início
        } else if (!isCellPhone && value.length >= 9) { 
            // Se for fixo, formata como (XX) XXXX-XXXX
            value = value.replace(/(\d{4})(\d)/, '$1-$2'); // Formata fixo com 4 dígitos no início
        }

        inputElement.value = value;
    });
}

async function createForms() {
    const data = {
        "estadoSolicitacao": "criada",
        "nome": forms[0][0][3],
        "pseudonimo": forms[0][1][3],
        "telefone": forms[1][1][3],
        "data_nascimento": String(forms[0][2][3]),
        "informacao_de_contato": forms[1][1][3],
        "primeira_solicitacao": true,
        "motivo": forms[3][0][3],
        "sintomas": forms[4][6][3],
        "doencas": forms[4][7][3],
        "medicamentos": forms[4][3][3],
        "tratamentos": forms[4][2][3],
        "alergias": forms[4][4][3],
        "religioes": forms[3][1][3],
        "generos": forms[0][4][3],
        "sexo": forms[0][3][3],
        "endereco_cep": forms[2][0][3],
        "endereco_estado": forms[2][1][3],
        "endereco_cidade": forms[2][2][3],
        "endereco_bairro": forms[2][3][3],
        "endereco_logradouro": forms[2][4][3],
        "endereco_numero": forms[2][5][3],
        "endereco_complemento": forms[2][6][3],
        "ja_fez_psicoterapia": forms[4][11][3] == "Sim"? true : false,
        "ja_fez_pisiquiatrico": forms[4][12][3] == "Sim"? true : false,
        "ja_fez_tratamento_espirita": forms[4][13][3] == "Sim"? true : false
    };
    
    console.log(data);
    const record = await pb.collection('solicitacoes').create(data);
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
    content += `<div class="${pageIndex == 0? "d-none" :  "col-md-6 col-12 mb-md-0 mb-3 p-0"}">  <div class="button secondary d-flex align-items-center justify-content-center fit-w" onclick="buildForms('-')"><h4 class="me-3">Voltar</h4><i data-feather="chevron-left"></i></div>  </div>`;
    content += `<div class="${pageIndex == 0? "col-12" : "col-md-6 col-12 p-0"}">  <div class="button d-flex align-items-center justify-content-center fit-w" ${pageIndex == 5? "onclick=createForms()" : "onclick=buildForms('+')"}><h4 class="me-3">${pageIndex == 5? "Concluir" : "Continuar"}</h4><i data-feather="chevron-right"></i></div>  </div>`;
    content += `</div>`
    
    console.log(pageIndex);
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

buildForms(pageIndex);

setInterval(() => {
    timer -= 1;
}, 1000)