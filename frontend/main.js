let currentIndex = 0;

document.addEventListener("DOMContentLoaded", () => {
	buildForms(0);
});

let forms = {
	0: [
		["text", "user", "Nome completo", ""],
		["text", "user", "Nome social", ""],
		["date", "calendar", "Data de Nascimento", ""],
		["text", "user", "Sexo", ""],
		["email", "at-sign", "E-mail", ""],
		["text", "phone", "Telefone", ""],
		["text", "phone", "Telefone Secundário", ""],
		["text", "user", "EXEMPLO", ""],
	],
	1: [
		["text", "map", "Estado", ""],
		["text", "map", "Cidade", ""],
		["text", "map", "Bairro", ""],
		["text", "map-pin", "Endereço", ""],
		["text", "map-pin", "Número", ""],
		["text", "map-pin", "Complemento", ""],
	],
	2: [
		["text", "smile", "Qual é o motivo da solicitação?", ""],
		["checkbox", "tablet", "Possuo religião", ""],
	],
};

function buildInput(inputType, icon, placeholder, value) {
	return `
        <div class="form-area d-flex align-items-center mb-3 px-3">
			<i data-feather="${icon}" class="me-3"></i>
			<input class="text-input ${inputType != "checkbox"? "stretch-x" : ""}" type="${inputType}" value="${value}" placeholder="${placeholder}" />
		</div>
    	`;
}

function buildForms(stepIndex) {
	if (stepIndex == "+") stepIndex = currentIndex + 1;
	if (stepIndex == "-") stepIndex = currentIndex - 1;

	const formsElement = document.getElementById("forms");
	const formData = forms[stepIndex];
	let html = "";
	let title = "";

	if (!formData) return;
	const currentStepElement = document.getElementById(`step${currentIndex}`);
	currentStepElement.classList.remove("selected");
	const targetStepElement = document.getElementById(`step${stepIndex}`);
	targetStepElement.classList.add("selected");
	currentIndex = stepIndex;

	switch (stepIndex) {
		case 0: title = "Dados pessoais"; break;
		case 1: title = "Endereço"; break;
		case 2: title = "Dados Extras"; break;
		case 3: title = "Tratamentos e Sintomas"; break;
		case 4: title = "Termos"; break;
	}

	html += `<h1 class="mb-5">${title}</h1>`;

	formData.forEach(inputData => {
		const [inputType, icon, placeholder, value] = inputData;
		html += buildInput(inputType, icon, placeholder, value);
	});

	html += `
	<div class="d-flex mt-4">
	${currentIndex > 0? 
		`
			<div class="button d-flex align-items-center justify-content-center ${currentIndex === 4 ? "stretch-x" : "stretch-x-half"}" onclick="buildForms('-')">
				<h4 class="me-3">Voltar</h4>
				<i data-feather="chevron-left"></i>
			</div>
		` : ""
	}
	${currentIndex < 4? 
		`
			<div class="button d-flex align-items-center justify-content-center ${currentIndex === 0 ? "stretch-x" : "stretch-x-half ms-auto"}" onclick="buildForms('+')">
				<h4 class="me-3">Continuar</h4>
				<i data-feather="chevron-right"></i>
			</div>
		` : ""
	}
	</div>
	`;

	formsElement.innerHTML = html;
	feather.replace();
}
