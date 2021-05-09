
let isFetching = false; 

const currentUrl = location.href;
const currentUrlArray = currentUrl.split('/')

const id = currentUrlArray[currentUrlArray.length - 1];

const attractionImageElement = document.getElementsByClassName('attraction-image')[0];
const nameElement = document.getElementsByClassName('name')[0];
const categoryMrtElement = document.getElementsByClassName('category-mrt')[0];
const descriptionElement = document.getElementsByClassName('description')[0];
const addressElement = document.getElementsByClassName('address')[0];
const transportElement = document.getElementsByClassName('transport')[0];
const circleAreaElement = document.getElementsByClassName('circle-area')[0];

const idInput = document.getElementById('idInput');
idInput.value = id;

const halfDayInput = document.querySelectorAll('[name=halfDay]');
const feeNumberElement = document.getElementsByClassName('fee-number')[0];
halfDayInput.forEach(halfDay => halfDay.addEventListener('change', priceShow));
function priceShow() {
   let halfDayChecked = document.querySelector('[name=halfDay]:checked');
   if (halfDayChecked.value === 'morning') {
      feeNumberElement.innerText = 2000;
   } else if (halfDayChecked.value === 'afternoon') {
      feeNumberElement.innerText = 2500;
   } 
}
priceShow();

const priceInput = document.getElementById('priceInput');
priceInput.value = feeNumberElement.innerText;

showAttraction();

function showAttraction() {
   isFetching = true;

   const src = srcDetermine(id);
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

function srcDetermine(id) {
   if (id >= 1) {
      return `../api/attraction/${id}`;
   } 
   return null;
}

function fetchAPI(src) {
   fetch(src)
      .then(response => response.json())
      .then((result) => {
         const attractionData = result.data;

         createDetermine(attractionData);
      })
      .then(() => {
            isFetching = false;
         }
      )
      .catch(error => console.log(error));
}

function createDetermine(attractionData) {
   if (attractionData == null) {
      const attractionIntroductionElement = document.getElementsByClassName('attraction-introduction')[0];
      const sectionElement = document.getElementsByTagName('section')[0];
      const hrElement = document.getElementsByTagName('hr')[0];

      removeAllChildNodes(attractionIntroductionElement);
      removeAllChildNodes(sectionElement);
      hrElement.remove();
   } else {
      createAPIElement(attractionData);

      carousel();
   }
}


function createAPIElement(attractionData) {
   let images = attractionData.images;
   let name = attractionData.name;
   let mrt = attractionData.mrt;
   if (!mrt) {
      mrt = '無';
   }
   let category = attractionData.category;
   let description = attractionData.description;
   let address = attractionData.address;
   let transport = attractionData.transport;
   if (!transport) {
      transport = '無';
   }
   
   removeAllChildNodes(attractionImageElement);
   removeAllChildNodes(nameElement);
   removeAllChildNodes(categoryMrtElement);
   removeAllChildNodes(descriptionElement);
   removeAllChildNodes(addressElement);
   removeAllChildNodes(transportElement);

   for (let image of images) {
      let imageElement = document.createElement('img');
      imageElement.src = image;

      let circleElement = document.createElement('div');
      circleElement.classList.add('circle');

      attractionImageElement.appendChild(imageElement);
      circleAreaElement.append(circleElement);
   }

   let nameContent = document.createTextNode(name);
   nameElement.appendChild(nameContent);

   let categoryMrtContent = document.createTextNode(`${category} at ${mrt}`);
   categoryMrtElement.appendChild(categoryMrtContent);

   let descriptionContent = document.createTextNode(description);
   descriptionElement.appendChild(descriptionContent);

   let addressContent = document.createTextNode(address);
   addressElement.appendChild(addressContent);

   let transportContent = document.createTextNode(transport);
   transportElement.appendChild(transportContent);
}

// carousel
const leftArrow = document.getElementById('left-arrow');
const rightArrow = document.getElementById('right-arrow');

function carousel() {
   const imageElementArray = Array.from(attractionImageElement.querySelectorAll('img'));
   const circleElementArray = Array.from(circleAreaElement.querySelectorAll('.circle'));
   
   let initialImageElement = imageElementArray[0];
   initialImageElement.classList.add('active');

   let initialCircleElement = circleElementArray[0];
   initialCircleElement.classList.add('active');
}

function lastImage() {
   const imageElementArray = Array.from(attractionImageElement.querySelectorAll('img'));
   const circleElementArray = Array.from(circleAreaElement.querySelectorAll('.circle'));

   const currentImageElement = attractionImageElement.getElementsByClassName('active')[0];
   const currentCircleElement = circleAreaElement.getElementsByClassName('active')[0];

   let lastImageElement = imageElementArray[imageElementArray.indexOf(currentImageElement) - 1];
   let lastCircleElement = circleElementArray[circleElementArray.indexOf(currentCircleElement) - 1];

   if (imageElementArray.indexOf(currentImageElement) - 1 < 0) {
      lastImageElement = imageElementArray[imageElementArray.length - 1];
   }
   if (circleElementArray.indexOf(currentCircleElement) - 1 < 0) {
      lastCircleElement = circleElementArray[circleElementArray.length - 1];
   }
   
   currentImageElement.classList.remove('active');
   lastImageElement.classList.add('active');

   currentCircleElement.classList.remove('active');
   lastCircleElement.classList.add('active');
}

function nextImage() {
   const imageElementArray = Array.from(attractionImageElement.querySelectorAll('img'));
   const circleElementArray = Array.from(circleAreaElement.querySelectorAll('.circle'));

   const currentImageElement = attractionImageElement.getElementsByClassName('active')[0];
   const currentCircleElement = circleAreaElement.getElementsByClassName('active')[0];

   let nextImageElement = imageElementArray[imageElementArray.indexOf(currentImageElement) + 1];
   let nextCircleElement = circleElementArray[circleElementArray.indexOf(currentCircleElement) + 1];

   if (imageElementArray.indexOf(currentImageElement) + 1 >= imageElementArray.length) {
      nextImageElement = imageElementArray[0];
   }
   
   if (circleElementArray.indexOf(currentCircleElement) + 1 >= circleElementArray.length) {
      nextCircleElement = circleElementArray[0];
   }
   
   currentImageElement.classList.remove('active');
   nextImageElement.classList.add('active');

   currentCircleElement.classList.remove('active');
   nextCircleElement.classList.add('active');
}

leftArrow.addEventListener('click', lastImage);
rightArrow.addEventListener('click', nextImage);
