
/* user name */
function getUser() {
   const src = '/api/user';
   fetch(src)
      .then(response => response.json())
      .then(result => {
         const userData = result.data;
         if (userData) {
/*             const welcomeElement = document.createElement('div');
            welcomeElement.classList.add('welcome');
            
            const bookingElement = document.getElementsByClassName('booking')[0];
            const bookingAttractionElement = document.getElementsByClassName('booking-attraction')[0];
            bookingElement.insertBefore(welcomeElement, bookingAttractionElement); */

            const welcomeElement = document.getElementsByClassName('welcome')[0];

            const welcomeContent = document.createTextNode(`您好，${userData.name}，待預訂的行程如下：`);
            welcomeElement.appendChild(welcomeContent);
         } else {
            return;
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

   let imageElement = document.createElement('img');
   imageElement.src = image;
   attractionImageElement.appendChild(imageElement);

   let nameContent = document.createTextNode(`台北一日遊：${name}`);
   attractionNameElement.appendChild(nameContent);

   let dateContent = document.createTextNode(date);
   dateElement.appendChild(dateContent);

   let timeContent = document.createTextNode(actualTime);
   timeElement.appendChild(timeContent);

   let feeContent = document.createTextNode(`新台幣 ${price} 元`);
   feeElement.appendChild(feeContent);

   let addressContent = document.createTextNode(address);
   addressElement.appendChild(addressContent);
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
      alert('刪除成功');
   } else {
      return;
   }
}