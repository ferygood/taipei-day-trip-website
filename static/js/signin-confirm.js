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