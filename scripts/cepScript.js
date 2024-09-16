// Função para habilitar ou desabilitar campos
function alternarCamposEndereco() {
  const isCheckboxChecked = document.getElementById('semCep').checked;
  document.getElementById('cep').disabled = isCheckboxChecked;
  //document.getElementById('estado').disabled = !isCheckboxChecked;
  //document.getElementById('cidade').disabled = !isCheckboxChecked;

  if (isCheckboxChecked) {
    document.getElementById('cep').value = '';
    document.getElementById('bairro').value = '';
    document.getElementById('logradouro').value = '';
    carregarEstados(); // Carregar estados ao marcar a checkbox
  } else {
    document.getElementById('estado').value = '';
    document.getElementById('cidade').value = '';
    document.getElementById('bairro').value = '';
    document.getElementById('logradouro').value = '';
  }
}

// Função para formatar o CEP com ponto e hífen
function formatarCep(input) {
  // Remove tudo que não é dígito
  let valor = input.value.replace(/\D/g, '');

  // Adiciona o ponto e o hífen na posição correta
  if (valor.length > 5) {
    valor = valor.replace(/(\d{2})(\d{3})(\d{0,3})/, '$1.$2-$3');
  } else if (valor.length > 2) {
    valor = valor.replace(/(\d{2})(\d{0,3})/, '$1.$2');
  }

  // Atualiza o valor do input
  input.value = valor;
}

// Evento para preencher automaticamente os campos com o CEP ao pressionar 'Enter'
function eventoEnterCep(event) {
  const key = event.key;
  if (key === 'Enter') {
    document.getElementById('cep').blur();
  }
}

// Variáveis para armazenar a posição atual na lista
let estadoSelecionadoIndex = -1;
let cidadeSelecionadaIndex = -1;

// Função para mover a seleção na lista de estados
function navegarListaEstados(event) {
  const listaEstados = document.getElementById('listaEstados');
  const items = listaEstados.getElementsByTagName('li');

  if (event.key === 'ArrowDown') {
    estadoSelecionadoIndex = (estadoSelecionadoIndex + 1) % items.length;
    items[estadoSelecionadoIndex].scrollIntoView({ block: 'nearest' });
  } else if (event.key === 'ArrowUp') {
    estadoSelecionadoIndex =
      (estadoSelecionadoIndex - 1 + items.length) % items.length;
    items[estadoSelecionadoIndex].scrollIntoView({ block: 'nearest' });
  } else if (event.key === 'Enter') {
    items[estadoSelecionadoIndex].click();
    estadoSelecionadoIndex = -1;
  }

  // Atualiza a classe dos itens para refletir a seleção
  Array.from(items).forEach((item, index) => {
    item.classList.toggle('selecionado', index === estadoSelecionadoIndex);
  });
}

// Função para mover a seleção na lista de cidades
function navegarListaCidades(event) {
  const listaCidades = document.getElementById('listaCidades');
  const items = listaCidades.getElementsByTagName('li');

  if (event.key === 'ArrowDown') {
    cidadeSelecionadaIndex = (cidadeSelecionadaIndex + 1) % items.length;
    items[cidadeSelecionadaIndex].scrollIntoView({ block: 'nearest' });
  } else if (event.key === 'ArrowUp') {
    cidadeSelecionadaIndex =
      (cidadeSelecionadaIndex - 1 + items.length) % items.length;
    items[cidadeSelecionadaIndex].scrollIntoView({ block: 'nearest' });
  } else if (event.key === 'Enter') {
    items[cidadeSelecionadaIndex].click();
    cidadeSelecionadaIndex = -1;
  }

  // Atualiza a classe dos itens para refletir a seleção
  Array.from(items).forEach((item, index) => {
    item.classList.toggle('selecionado', index === cidadeSelecionadaIndex);
  });
}

// Adicionar eventos de teclado para navegação
document
  .getElementById('estado')
  .addEventListener('keydown', navegarListaEstados);
document
  .getElementById('cidade')
  .addEventListener('keydown', navegarListaCidades);

// Função para fechar as listas suspensas
function fecharListas() {
  document.getElementById('listaEstados').style.display = 'none';
  document.getElementById('listaCidades').style.display = 'none';
}

// Adiciona o evento de clique ao documento para fechar as listas
document.addEventListener('click', function (event) {
  const listaEstados = document.getElementById('listaEstados');
  const listaCidades = document.getElementById('listaCidades');
  const estadoInput = document.getElementById('estado');
  const cidadeInput = document.getElementById('cidade');

  // Verifica se o clique foi fora dos inputs de estado e cidade
  if (
    !estadoInput.contains(event.target) &&
    !listaEstados.contains(event.target)
  ) {
    listaEstados.style.display = 'none';
  }

  if (
    !cidadeInput.contains(event.target) &&
    !listaCidades.contains(event.target)
  ) {
    listaCidades.style.display = 'none';
  }
});

// Evento para preencher campos ao inserir CEP
document.getElementById('cep').addEventListener('blur', function () {
  var cep = this.value.replace(/\D/g, '');

  if (cep.length == 8) {
    fetch(`https://viacep.com.br/ws/${cep}/json/`)
      .then(response => response.json())
      .then(data => {
        if (!('erro' in data)) {
          document.getElementById('estado').value = data.uf;
          document.getElementById('cidade').value = data.localidade;
          document.getElementById('bairro').value = data.bairro;
          document.getElementById('logradouro').value = data.logradouro;
        } else {
          alert('CEP não encontrado.');
        }
      })
      .catch(error => console.error('Erro ao buscar o CEP:', error));
  }
});

// Função para buscar e preencher os campos de endereço com base no CEP
function buscarEnderecoPorCep() {
  const cep = document.getElementById('cep').value.replace(/\D/g, '');
  if (cep.length === 8) {
    fetch(`https://viacep.com.br/ws/${cep}/json/`)
      .then(response => response.json())
      .then(data => {
        if (!data.erro) {
          // Preenche os campos com os dados retornados
          document.getElementById('estado').value = data.uf;
          document.getElementById('cidade').value = data.localidade;
          document.getElementById('bairro').value = data.bairro;
          document.getElementById('logradouro').value = data.logradouro;

          // Atualiza as cidades com base na sigla do estado
          atualizarCidadesPorSigla(data.uf);

          // Oculta a lista de cidades, caso esteja visível
          document.getElementById('listaCidades').style.display = 'none';
        } else {
          alert('CEP não encontrado.');
        }
      })
      .catch(error => console.error('Erro ao buscar o CEP:', error));
  }
}

// Função para atualizar cidades com base no estado selecionado
function atualizarCidades(estadoId) {
  const cidadeInput = document.getElementById('cidade');
  const listaCidades = document.getElementById('listaCidades');
  listaCidades.innerHTML = ''; // Limpa as cidades anteriores

  if (estadoId) {
    fetch(
      `https://servicodados.ibge.gov.br/api/v1/localidades/estados/${estadoId}/municipios`
    )
      .then(response => response.json())
      .then(cidades => {
        todasAsCidades = cidades; // Armazena as cidades na variável global
        cidadeInput.disabled = false;
        filtrarCidades(); // Atualiza a lista de cidades
      })
      .catch(error => console.error('Erro ao buscar cidades:', error));
  }
}

let todosOsEstados = [];
let todasAsCidades = [];

// Função para carregar os estados ao carregar a página
function carregarEstados() {
  fetch('https://servicodados.ibge.gov.br/api/v1/localidades/estados')
    .then(response => response.json())
    .then(estados => {
      estados.sort((a, b) => a.sigla.localeCompare(b.sigla)); // Ordena por sigla

      todosOsEstados = estados; // Armazena os estados na variável global
    })
    .catch(error => console.error('Erro ao carregar estados:', error));
}

// Função para filtrar os estados conforme o usuário digita
function filtrarEstados() {
  const input = document.getElementById('estado').value.toUpperCase();
  const listaEstados = document.getElementById('listaEstados');
  listaEstados.innerHTML = '';

  const estadosFiltrados = todosOsEstados.filter(estado =>
    estado.sigla.includes(input)
  );

  estadosFiltrados.forEach(estado => {
    const li = document.createElement('li');
    li.textContent = estado.sigla;
    li.setAttribute('data-id', estado.id);
    li.onclick = () => selecionarEstado(estado.sigla, estado.id);
    listaEstados.appendChild(li);
  });

  // Mostrar a lista de estados se houver resultados
  if (estadosFiltrados.length > 0) {
    listaEstados.style.display = 'block';
  } else {
    listaEstados.style.display = 'none';
  }
}

// Função para selecionar o estado e carregar as cidades
function selecionarEstado(sigla, id) {
  document.getElementById('estado').value = sigla;
  document.getElementById('listaEstados').innerHTML = '';
  document.getElementById('listaEstados').style.display = 'none';
  atualizarCidades(id);
}

// Função para atualizar cidades com base no estado selecionado
function atualizarCidades(estadoId) {
  const cidadeInput = document.getElementById('cidade');
  const listaCidades = document.getElementById('listaCidades');
  listaCidades.innerHTML = ''; // Limpa as cidades anteriores

  if (estadoId) {
    fetch(
      `https://servicodados.ibge.gov.br/api/v1/localidades/estados/${estadoId}/municipios`
    )
      .then(response => response.json())
      .then(cidades => {
        todasAsCidades = cidades; // Armazena as cidades na variável global
        cidadeInput.disabled = false;
        filtrarCidades(); // Atualiza a lista de cidades conforme o texto digitado
      })
      .catch(error => console.error('Erro ao buscar cidades:', error));
  }
}

// Função para atualizar cidades com base na sigla do estado
function atualizarCidadesPorSigla(estadoSigla) {
  const estadoSelecionado = todosOsEstados.find(
    estado => estado.sigla === estadoSigla
  );

  if (estadoSelecionado) {
    atualizarCidades(estadoSelecionado.id);
  }
}

// Função para filtrar as cidades conforme o usuário digita
function filtrarCidades() {
  const input = document.getElementById('cidade').value.toLowerCase();
  const listaCidades = document.getElementById('listaCidades');
  listaCidades.innerHTML = '';

  const cidadesFiltradas = todasAsCidades.filter(cidade =>
    cidade.nome.toLowerCase().includes(input)
  );

  cidadesFiltradas.forEach(cidade => {
    const li = document.createElement('li');
    li.textContent = cidade.nome;
    li.onclick = () => selecionarCidade(cidade.nome);
    listaCidades.appendChild(li);
  });

  // Mostrar a lista de cidades se houver resultados
  if (cidadesFiltradas.length > 0) {
    listaCidades.style.display = 'block';
  } else {
    listaCidades.style.display = 'none';
  }
}

// Função para selecionar a cidade
function selecionarCidade(nome) {
  document.getElementById('cidade').value = nome;
  document.getElementById('listaCidades').innerHTML = '';
  document.getElementById('listaCidades').style.display = 'none';
}

// Carregar estados ao carregar a página
window.onload = function () {
  carregarEstados();
  alternarCamposEndereco(); // Inicializa o estado dos campos
};
