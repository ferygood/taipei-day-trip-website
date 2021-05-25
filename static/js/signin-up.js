
// For Popup
const openModalButtons = document.querySelectorAll('[data-modal-target]');
const closeModalButtons = document.querySelectorAll('[data-close-button]');
const goSignupButton = document.querySelector('#goSignup');
const goSigninButton = document.querySelector('#goSignin');

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

goSignupButton.addEventListener('click', () => {
   const signinModal = document.getElementById('modalSignin');
   const signupModal = document.getElementById('modalSignup');

   closeModal(signinModal);
   openModal(signupModal);
});

goSigninButton.addEventListener('click', () => {
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

// For signin & signup Authentication
const signupForm = document.getElementById('signupForm');
const signinForm = document.getElementById('signinForm');

signupForm.addEventListener('submit', e => {
   e.preventDefault();

   signupCheck();
});

signinForm.addEventListener('submit', e => {
   e.preventDefault();

   signinCheck();
});

function signupCheck() {
   const nameElement = document.getElementById('signupName');
   const emailElememt = document.getElementById('signupEmail');
   const passwordElement = document.getElementById('signupPassword');

   /* 資料驗證，待進行 */
   if (passwordElement.value.length < 4) {
      return;
   }
   /* 加密，待進行 */

   const src = '/api/user';
   fetch(src, {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json'
      },
      body: JSON.stringify({
         "name": nameElement.value,
         "email": emailElememt.value,
         "password": passwordElement.value
      })
   })
      .then(response => response.json())
      .then(result => {
         const signupSuccess = result['ok'];
         const signupFailed = result['error'];

         const signupMessageElement = document.getElementById('signupMessage');
         signupMessageElement.innerText = '';
         signupMessageElement.classList.remove('show');
         if (signupSuccess) {
            signupMessageElement.classList.add('show');
            signupMessageElement.innerText = '註冊成功';
            signupMessageElement.style.color = 'green';

            nameElement.value = '';
            nameElement.innerText = '';
            emailElememt.value = '';
            emailElememt.innerText = '';
            passwordElement.value = '';
            passwordElement.innerText = '';
         }

         if (signupFailed) {
            signupMessageElement.innerText = result['message'];
            signupMessageElement.classList.add('show');

            nameElement.value = '';
            nameElement.innerText = '';
            emailElememt.value = '';
            emailElememt.innerText = '';
            passwordElement.value = '';
            passwordElement.innerText = '';
         }
      })
      .catch(err => console.log('錯誤', err));
}

function signinCheck() {
   const emailElememt = document.getElementById('signinEmail');
   const passwordElement = document.getElementById('signinPassword');

   /* 資料驗證，待進行 */
   if (passwordElement.value.length < 4) {
      return;
   }

   /* 加密，待進行 */
   
   const src = '/api/user';
   fetch(src, {
      method: 'PATCH',
      headers: {
         'Content-Type': 'application/json'
      },
      body: JSON.stringify({
         "email": emailElememt.value,
         "password": passwordElement.value
      })
   })
      .then(response => response.json())
      .then(result => {
         const signinSuccess = result['ok'];
         const signinFailed = result['error'];

         const signinMessageElement = document.getElementById('signinMessage');
         signinMessageElement.innerText = '';
         signinMessageElement.classList.remove('show');

         if (signinSuccess) {
            signinMessageElement.innerText = '';
            signinMessageElement.classList.remove('show');

            location.reload();
            
            closeModalButtons.forEach(button => {
               const modal = button.closest('.modal'); 
               closeModal(modal);
            });
               
            emailElememt.value = '';
            emailElememt.innerText = '';
            passwordElement.value = '';
            passwordElement.innerText = '';
         }

         if (signinFailed) {
            signinMessageElement.innerText = result['message'];
            signinMessageElement.classList.add('show');

            emailElememt.value = '';
            emailElememt.innerText = '';
            passwordElement.value = '';
            passwordElement.innerText = '';
         }
      })
      .catch(err => console.log('錯誤', err));
}

function signout() {
   const yes = confirm('確定要登出嗎？');
   if (yes) {
      const src = '/api/user';
      fetch(src, {
         method: 'DELETE'
      })
         .then(response => response.json())
         .then(result => {
            const signoutSuccess = result['ok'];
            const signoutFailed = result['error'];
   
            if (signoutSuccess) {          
               location.reload(); 
            }
            if (signoutFailed) {
               alert(result['message']);
            }
         })
         .catch(err => console.log('錯誤', err));      
   } else {
      alert('您決定保持登入狀態');
   }
   
}

signoutButton.addEventListener('click', signout);