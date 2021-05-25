import { tappayDealWith } from './tappay.js';

let userId;

/* user name */
function getUser() {
   const src = '/api/user';
   fetch(src)
      .then(response => response.json())
      .then(result => {
         const userData = result.data;

         const welcomeElement = document.getElementsByClassName('welcome')[0];
         const nameElement = document.getElementById('name');
         const emailElememt = document.getElementById('email');

         if (userData) {
            welcomeElement.innerText = `您好，${userData.name}，待預訂的行程如下：`;

            nameElement.value = userData.name;
            nameElement.innerText = userData.name;

            emailElememt.value = userData.email;
            emailElememt.innerText = userData.email;

            userId = userData.id;
         } else {
/*             
            const bookingElement = document.getElementsByClassName('booking')[0];

            removeAllChildNodes(bookingElement);
 */
            parent.location.href = '/';
         }
      })
      .catch(error => console.log(error));
}

getUser();

/* attraction information */
const attractionImageElement = document.getElementsByClassName('attraction-image')[0];
const attractionNameElement = document.getElementsByClassName('name')[0];
const dateElement = document.getElementsByClassName('date')[0];
const timeElement = document.getElementsByClassName('time')[0];
const feeElement = document.getElementsByClassName('fee')[0];
const addressElement = document.getElementsByClassName('address')[0];

showBooking();

function showBooking() {
   const src = '/api/booking';
   if (!src) {
      return;
   }
   fetchAPI(src);
}

function removeAllChildNodes(parent) {
   while (parent.firstChild) {
      parent.removeChild(parent.firstChild);
   }
}

function fetchAPI(src) {
   fetch(src)
      .then(response => response.json())
      .then(result => {
         const bookingData = result.data;

         createDetermine(bookingData);
      })
      .catch(error => console.log(error));
}

function createDetermine(bookingData) {
   if (bookingData == null) {
      const bookingElement = document.getElementsByClassName('booking')[0];

      removeAllChildNodes(bookingElement);

      const noResultElement = document.createElement('div');
      const noResultContent = document.createTextNode('目前沒有任何待預訂的行程');
      noResultElement.appendChild(noResultContent);
      bookingElement.appendChild(noResultContent);
   } else {
      createAPIElement(bookingData);
   }
}


function createAPIElement(bookingData) {
   const id = bookingData.attraction.id;
   const image = bookingData.attraction.image;
   const name = bookingData.attraction.name;
   const date = bookingData.date;
   const time = bookingData.time;
   let actualTime;
   if (time === 'morning') {
      actualTime = '早上 9 點到中午 12 點';
   }
   if (time === 'afternoon') {
      actualTime = '中午 12 點到下午 4 點';
   }
   const price = bookingData.price;
   const address = bookingData.attraction.address;

   document.getElementById('attraction-id').value = id;

   let imageElement = document.createElement('img');
   imageElement.src = image;
   attractionImageElement.appendChild(imageElement);
   document.getElementById('attraction-image').value = image;

   let nameContent = document.createTextNode(`台北一日遊：${name}`);
   attractionNameElement.appendChild(nameContent);
   document.getElementById('attraction-name').value = name;

   let dateContent = document.createTextNode(date);
   dateElement.appendChild(dateContent);
   document.getElementById('date').value = date;

   let timeContent = document.createTextNode(actualTime);
   timeElement.appendChild(timeContent);
   document.getElementById('time').value = time;

   let feeContent = document.createTextNode(`新台幣 ${price} 元`);
   feeElement.appendChild(feeContent);

   let addressContent = document.createTextNode(address);
   addressElement.appendChild(addressContent);
   document.getElementById('address').value = address;

   const totalPriceElement = document.getElementsByClassName('total-price')[0];
   totalPriceElement.innerText = `總價：新台幣 ${price} 元`;
   document.getElementById('total-price').value = price;
}

/* delete icon */
const deleteIcons = document.getElementsByClassName('delete-icon');

Array.from(deleteIcons).forEach(deleteIcon => {
   deleteIcon.addEventListener('click', deleteBooking);
});

function deleteBooking() {
   const yes = confirm('您確定要刪除嗎');

   if (yes) {
      this.parentElement.remove();

      const src = '/api/booking';
      fetch(src, {
         method: 'DELETE',
         headers: {
            'Content-Type': 'application/json'
         },
         body: JSON.stringify({
            "userId": userId,
         })
      })
         .then(response => response.json())
         .then(result => {
            const deleteSuccess = result['ok'];
            const deleteFailed = result['error'];

            if (deleteSuccess) {
               location.reload();
            }
            if (deleteFailed) {
               alert(result['message']);
            }
         })
         .catch(err => console.log('錯誤', err));
   } else {
      return;
   }
}

/* go /api/order */
const orderForm = document.getElementById('order-form');
orderForm.addEventListener('submit', e => {
   e.preventDefault();

   goOrder();
})

function goOrder() {
   const yes = confirm('您確定要訂購此行程並付款嗎？');

   // TBD
   const prime = 'adgb45f6';

   const price = document.getElementById('total-price').value;

   const attractionId = docuement.getElementById('attraction-id').value;
   const attractionName = docuement.getElementById('attraction-name').value;
   const address = docuement.getElementById('address').value;
   const image = docuement.getElementById('attraction-image').value;

   const date = document.getElementById('date').value;
   const time = document.getElementById('time').value;

   const name = document.getElementById('name').value;
   const email = docuement.getElementById('email').value;
   const phoneNumber = document.getElementById('phone-number').value;

   if (yes) {
      const src = '/api/booking';
      fetch(src, {
         method: 'POST',
         headers: {
            'Content-Type': 'application/json'
         },
         body: JSON.stringify({
            "prime": prime,
            "order": {
               "price": price,
               "trip": {
                  "attraction": {
                     "id": attractionId,
                     "name": attractionName,
                     "address": address,
                     "image": image
                  },
                  "date": date,
                  "time": time
               },
               "contact": {
                  "name": name,
                  "email": email,
                  "phone": phoneNumber
               }
            }
         })
      })
         .then(response => response.json())
         .then(result => {

         })
         .catch(err => console.log('錯誤', err));
   } else {
      return;
   }
}
