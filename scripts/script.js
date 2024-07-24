/*
 ** Este código verifica se o campo 'SIM' foi marcado para exibir o conteúdo oculto.
 */

// Função para alternar a visibilidade do campo de texto de religião
function toggleCampoTexto() {
  const checkboxReligiao = document.getElementById('religiao_sim');
  const campoTexto = document.getElementById('campoTexto');
  campoTexto.style.display = checkboxReligiao.checked ? 'block' : 'none';
}

// Função para alternar a visibilidade do campo de texto de tratamento médico
function toggleCampoTramentoMedico() {
  const checkboxTratamentoMedico = document.getElementById(
    'tratamento_medico_sim'
  );
  const campoTratamentoMedico = document.getElementById(
    'campoTratamentoMedico'
  );
  campoTratamentoMedico.style.display = checkboxTratamentoMedico.checked
    ? 'block'
    : 'none';
}

// Função para alternar a visibilidade do campo de texto de medicamento
function toggleCampoMedicamento() {
  const checkboxMedicamento = document.getElementById('medicamento_sim');
  const campoMedicamento = document.getElementById('campoMedicamento');
  campoMedicamento.style.display = checkboxMedicamento.checked
    ? 'block'
    : 'none';
}

// Função para alternar a visibilidade do campo de texto de alergia
function toggleCampoAlergia() {
  const checkboxMedicamento = document.getElementById('alergia_sim');
  const campoMedicamento = document.getElementById('campoAlergia');
  campoMedicamento.style.display = checkboxMedicamento.checked
    ? 'block'
    : 'none';
}

// Função para alternar a visibilidade do campo de texto de tratamento psiquiátrico
function toggleCampoTratamentoPsiquiatrico() {
  const checkboxMedicamento = document.getElementById(
    'tratamento_psiquiatrico_sim'
  );
  const campoMedicamento = document.getElementById(
    'campoTratamentoPsiquiatrico'
  );
  campoMedicamento.style.display = checkboxMedicamento.checked
    ? 'block'
    : 'none';
}
