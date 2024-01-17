'use strict';

const modal = document.querySelector('.modal');
const closeModal = document.querySelector('.close-modal');
const showModal = document.querySelectorAll('.show-modal');
const layer = document.querySelector('.overlay');

for (let i = 0; i < showModal.length; i++) {
  showModal[i].addEventListener('click', function () {
    modal.classList.remove('hidden');
    layer.classList.remove('hidden');
  });
}
closeModal.addEventListener('click', function () {
  modal.classList.add('hidden');
  layer.classList.add('hidden');
});
layer.addEventListener('click', function () {
  modal.classList.add('hidden');
  layer.classList.add('hidden');
});
document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape' && !modal.classList.contains('hidden')) {
    modal.classList.add('hidden');
    layer.classList.add('hidden');
  }
});
