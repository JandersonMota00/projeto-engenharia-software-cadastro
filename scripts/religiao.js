document
  .getElementById('religionSelect')
  .addEventListener('change', function () {
    const selectedValue = this.value;
    if (selectedValue) {
      addReligionTag(selectedValue);
      this.value = ''; // Reseta a seleção após adicionar
    }
  });

function addReligionTag(religion) {
  // Verifica se a religião já foi adicionada
  const existingTags = document.querySelectorAll('.religion-tag');
  for (let tag of existingTags) {
    if (tag.textContent.trim() === religion) {
      return; // Não adiciona se já existir
    }
  }

  const tag = document.createElement('div');
  tag.className = 'religion-tag';
  tag.innerHTML =
    religion +
    ' <button class="remove-btn" onclick="removeReligionTag(this)">X</button>';

  document.getElementById('selectedReligions').appendChild(tag);
}

function removeReligionTag(button) {
  const tag = button.parentNode;
  document.getElementById('selectedReligions').removeChild(tag);
}
