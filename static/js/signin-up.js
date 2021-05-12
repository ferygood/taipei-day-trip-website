
// For Popup
const openModalButtons = document.querySelectorAll('[data-modal-target]');
const closeModalButtons = document.querySelectorAll('[data-close-button]');
const goSignupLink = document.querySelector('#goSignup');
const goSigninLink = document.querySelector('#goSignin');

const overlay = document.getElementById('overlay');

openModalButtons.forEach(button => {
   button.addEventListener('click', () => {
   // button.dataset.modalTarget = data-modal-target in HTML <button>
      const modal = document.querySelector(button.dataset.modalTarget); 
      openModal(modal);
   });
});

closeModalButtons.forEach(button => {
   button.addEventListener('click', () => {
      const modal = button.closest('.modal'); 
      closeModal(modal);
   });
});


overlay.addEventListener('click', () => {
   const modals = document.querySelectorAll('.modal.active');
   modals.forEach(modal => {
      closeModal(modal);
   });
});

goSignupLink.addEventListener('click', () => {
   const signinModal = document.getElementById('modalSignin');
   const signupModal = document.getElementById('modalSignup');

   closeModal(signinModal);
   openModal(signupModal);
});

goSigninLink.addEventListener('click', () => {
   const signinModal = document.getElementById('modalSignin');
   const signupModal = document.getElementById('modalSignup');

   closeModal(signupModal);
   openModal(signinModal);
});

function openModal(modal) {
   if (modal == null) return
   modal.classList.add('active');
   overlay.classList.add('active');
}

function closeModal(modal) {
   if (modal == null) return
   modal.classList.remove('active');
   overlay.classList.remove('active');
}

// For signin-authentication

