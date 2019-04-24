const file = document.getElementById('file');
const label = document.getElementById('filelabel');
const btn = document.getElementById('submitBtn');

let isFile = false;

file.addEventListener('input', (event) => {
  const name = file.files[0].name;
  if (name) {
    isFile = true;
    label.innerText = file.files[0].name;
    btn.disabled = false;
  } else {
    isFile = false;
    label.innerText = 'Обрати файл...';
    btn.disabled = true;
  }
});
