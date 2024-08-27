let forms = [
	[["Dados pessoais"], ["text", "user", "Nome completo", ""], ["text", "user", "Nome social", ""], ["date", "calendar", "Data de Nascimento", ""], ["dropdown", "user", "Sexo", ""]],
	[["Meios de Contato"], ["email", "at-sign", "E-mail", ""], ["text", "phone", "Telefone", ""], ["checkbox", "phone", "Whatsapp", false], ["checkbox", "phone", "Telegram", false], ["text", "phone", "Telefone Emergencial", ""], ["checkbox", "phone", "Whatsapp", false], ["checkbox", "phone", "Telegram", false]],
	[["Endereço"], ["text", "map", "Estado", ""], ["text", "map", "Cidade", ""], ["text", "map", "Bairro", ""], ["text", "map-pin", "Endereço", ""], ["text", "map-pin", "Número", ""], ["text", "map-pin", "Complemento", ""]],
	[["Dados Extras"], ["text", "smile", "Qual é o motivo da solicitação?", ""], ["checkbox", "tablet", "Possuo religião", ""]],
	[
		["Tratamentos"],
		["checkbox", "tablet", "Estou fazendo algum tratamento médico", false],
		["checkbox", "tablet", "Faço uso de medicamentos", false],
		["checkbox", "tablet", "Eu desmaio sem causa aparente", false],
		["checkbox", "tablet", "Eu vejo vultos", false],
		["checkbox", "tablet", "Eu escuto vozes", false],
		["checkbox", "tablet", "Tenho pensamentos negativos / suicidas", false],
		["checkbox", "tablet", "Houve desencarne em minha família recentemente", false],
		["checkbox", "tablet", "Eu tenho alergias", false],
		["checkbox", "tablet", "Faço psicoterapia", false],
		["checkbox", "tablet", "Fiz / Faço tratamento psiquiátrico", false],
		["checkbox", "tablet", "Eu já fiz tratamento espiritual", false],
	],
	[["Termos"],["checkbox", "smile", "Ciente", false]]
];

let pageIndex = 0;

document.addEventListener("DOMContentLoaded", () => {
	buildForms(pageIndex);
});

function buildInput(inputType, icon, placeholder, value, index) {
	let html = "";
	switch (inputType) {
		case "dropdown":
			html += `<div class="form-area d-flex align-items-center mb-3 px-3"><i data-feather="${icon}" class="me-3"></i><select class="form-area stretch-x" onchange="changeValue(${index})"><option value="">Gênero</option><option value="opcao1">Masculino</option><option value="opcao2">Feminino</option><option value="opcao3">Outro</option></select></div>`;
			break;
		case "checkbox":
			if (pageIndex == 1 && (index == 3 || index == 6)) html += `<div class="d-flex checkboxes">`;
			html += `<div class="form-area d-flex align-items-center mb-3 px-3"><i data-feather="${icon}" class="me-3"></i><input type="checkbox" id="checkbox-${index}" onchange="changeValue(${index})" /><label for="checkbox-${index}" class="ms-2">${placeholder}</label></div>`;
			if (pageIndex == 1 && (index == 4 || index == 7)) html += `</div>`;
			break;
		default:
			html += `<div class="form-area d-flex align-items-center mb-3 px-3"><i data-feather="${icon}" class="me-3"></i><input class="text-input ${inputType != "checkbox" ? "stretch-x" : ""}" type="${inputType}" value="${value}" placeholder="${placeholder}" onchange="changeValue(${index})"/></div>`;
			break;
	}

	return html;
}

function buildForms(index) {
	if (index == "+") index = pageIndex + 1;
	if (index == "-") index = pageIndex - 1;

	const element = document.getElementById("forms");
	const formData = forms[index];
	let content = "";

	if (!formData) return;

	const currentStepElement = document.getElementById(`step_${pageIndex}`);
	currentStepElement.classList.remove("selected");
	const targetStepElement = document.getElementById(`step_${index}`);
	targetStepElement.classList.add("selected");

	pageIndex = index;

	content += `<h1 class="mb-5">${forms[pageIndex][0]}</h1>`;

	formData.forEach((data, index) => {
		if (index > 0) {
			const [inputType, icon, placeholder, value] = data;
			content += buildInput(inputType, icon, placeholder, value, index);
		}
	});

	content += `<div class="d-flex mt-4">`;
	if (pageIndex > 0) content += `<div class="button d-flex align-items-center justify-content-center ${pageIndex == forms.length ? "stretch-x" : "stretch-x-half"}" onclick="buildForms('-')"><h4 class="me-3">Voltar</h4><i data-feather="chevron-left"></i></div>`;
	if (pageIndex < forms.length - 1) content += `<div class="button d-flex align-items-center justify-content-center ${pageIndex == 0 ? "stretch-x" : "stretch-x-half ms-auto"}" onclick="buildForms('+')"><h4 class="me-3">Continuar</h4><i data-feather="chevron-right"></i></div>`;

	element.innerHTML = content;
	feather.replace();
}
