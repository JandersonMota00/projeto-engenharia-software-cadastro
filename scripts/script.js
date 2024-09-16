/*
 ** Este código verifica se o campo 'SIM' foi marcado para exibir o conteúdo oculto.
 */

// Função para alternar a visibilidade do campo de texto de religião
function alternarCampoTexto() {
  const radioReligiaoSim = document.getElementById('religiao_sim');
  const campoTexto = document.getElementById('campoTexto');
  const textoArea = document.getElementById('religiao_texto');

  if (radioReligiaoSim.checked) {
    campoTexto.style.display = 'block';
    textoArea.required = true;
  } else {
    campoTexto.style.display = 'none';
    textoArea.value = ''; // Limpa o conteúdo do campo textarea
    textoArea.required = false;
  }
}

// Função para alternar a visibilidade do campo de texto de tratamento médico
function alternarCampoTramentoMedico() {
  const radioTratamentoMedicoSim = document.getElementById(
    'tratamento_medico_sim'
  );
  const campoTratamentoMedico = document.getElementById(
    'campoTratamentoMedico'
  );
  const textarea = campoTratamentoMedico.querySelector('textarea');

  if (radioTratamentoMedicoSim.checked) {
    campoTratamentoMedico.style.display = 'block';
  } else {
    campoTratamentoMedico.style.display = 'none';
    textarea.value = ''; // Apaga o conteúdo do textarea
  }
}

// Função para alternar a visibilidade do campo de texto de medicamento
function alternarCampoMedicamento() {
  const radioMedicamentoSim = document.getElementById('medicamento_sim');
  const radioMedicamentoNao = document.getElementById('medicamento_nao');
  const campoMedicamento = document.getElementById('campoMedicamento');
  const textareaMedicamento = document.getElementById('medicamento_texto');

  if (radioMedicamentoSim.checked) {
    campoMedicamento.style.display = 'block';
  } else if (radioMedicamentoNao.checked) {
    campoMedicamento.style.display = 'none';
    textareaMedicamento.value = ''; // Apaga o texto do textarea
  }
}

// Função para alternar a visibilidade do campo de texto de alergia
function alternarCampoAlergia() {
  const radioSim = document.getElementById('alergia_sim');
  const campoAlergia = document.getElementById('campoAlergia');
  const textarea = campoAlergia.querySelector('textarea');

  if (radioSim.checked) {
    campoAlergia.style.display = 'block';
  } else {
    campoAlergia.style.display = 'none';
    textarea.value = ''; // Limpa o conteúdo do textarea
  }
}

// Função para alternar a visibilidade do campo de texto de tratamento psiquiátrico
function alternarCampoTratamentoPsiquiatrico() {
  const radioSim = document.getElementById('tratamento_psiquiatrico_sim');
  const radioNao = document.getElementById('tratamento_psiquiatrico_nao');
  const campoTratamento = document.getElementById(
    'campoTratamentoPsiquiatrico'
  );
  const textarea = document.getElementById('textareaTratamentoPsiquiatrico');

  if (radioSim.checked) {
    campoTratamento.style.display = 'block';
  } else {
    campoTratamento.style.display = 'none';
    textarea.value = ''; // Limpa o conteúdo do textarea
  }
}

// Função para verificar e corrigir o campo telefone
document.addEventListener('DOMContentLoaded', () => {
  const inputsTel = document.getElementsByClassName('inputs-cel');
  for (const inputTel of inputsTel) {
    inputTel.addEventListener('input', formatarTelefone);
  }

  function formatarTelefone(event) {
    let value = event.target.value;

    value = value.replace(/\D/g, '');

    if (value.length > 11) {
      value = value.slice(0, 11);
    }
    const formattedValue = value
      .replace(/(\d{2})(\d)/, '($1) $2')
      .replace(/(\d{5})(\d)/, '$1-$2');

    event.target.value = formattedValue;
  }
});
