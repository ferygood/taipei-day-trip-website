const signinButton = document.getElementById('signinButton');
const signoutButton = document.getElementById('signoutButton');

/* singin confirm */
function signinConfirm() {
   const src = '/api/user';
   fetch(src)
      .then(response => response.json())
      .then(result => {
         const userData = result.data;
         if (userData) {
            signinButton.classList.add('hidden');
            signoutButton.classList.remove('hidden');
         } else {
            signinButton.classList.remove('hidden');
            signoutButton.classList.add('hidden');
         }
      })
      .catch(error => console.log(error));
}

signinConfirm();

/* For /booking authentication */
const bookingLink = document.getElementById('booking-link');
bookingLink.addEventListener('click', e => {
   e.preventDefault();

   signinPopup();
})

function signinPopup() {
   const src = '/api/user';
   fetch(src)
      .then(response => response.json())
      .then(result => {
         const userData = result.data;
         if (userData) {
            parent.location.href = '/booking';
         } else {
            const openModalButtons = document.querySelectorAll('[data-modal-target]');
   
            openModalButtons.forEach(button => {
               const modal = document.querySelector(button.dataset.modalTarget); 
               openModal(modal);
            });
         }
      })
      .catch(error => console.log(error));
}

function openModal(modal) {
   if (modal == null) return
   modal.classList.add('active');
   overlay.classList.add('active');
}
