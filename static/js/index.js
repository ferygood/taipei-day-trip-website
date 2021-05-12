
// display attractions
let page = 0;

// Detect Fetching or not
let isFetching = false;

// search form
const searchform = document.getElementById('searchform');

searchform.addEventListener('submit', (e) => {
   e.preventDefault();

   const mainElement = document.getElementsByClassName('main')[0];

   removeAllChildNodes(mainElement);

   page = 0;

   search();
});

const searchInput = document.getElementById('searchInput');
searchInput.addEventListener('keyup', e => {
   if (e.code == 'Enter') {
      e.preventDefault();
      document.getElementById('searchInput').blur();
   }
})

search();

function search() {
   isFetching = true;

   let keyword = document.getElementsByName('keyword')[0].value;

   const src = srcDetermine(page, keyword);
   if (!src) return;

   fetchAPI(src);
}

function removeAllChildNodes(parent) {
   while (parent.firstChild) {
      parent.removeChild(parent.firstChild);
   }
}   

function srcDetermine(page, keyword) {
   if (page != null && keyword) {
      return `api/attractions?page=${page}&keyword=${keyword}`;
   }
   if (page != null) {
      return `api/attractions?page=${page}`;
   }
   return null;
}

function fetchAPI(src) {
   fetch(src)
      .then(response => response.json())
      .then((result) => {
         let attractionDataArray = result.data;
         let nextPage = result.nextPage;
         
         const mainElement = document.getElementsByClassName('main')[0];

         createDetermine(attractionDataArray, mainElement);
         page = nextPage;
      })
      .then(() => {
            isFetching = false;
         }
      )
      .catch(error => console.log(error));
}

function createDetermine(attractionDataArray, mainElement) {
   if (attractionDataArray == null) {
      const titleElement = createNoResultElement();

      mainElement.appendChild(titleElement);
   } else {
         for (let attractionData of attractionDataArray) {
            let attractionElement = document.createElement('a');
            attractionElement.classList.add('attraction');
            mainElement.appendChild(attractionElement);
         
            createAPIElement(attractionData, attractionElement);          
         }
      } 
}

function createAPIElement(attractionData, attractionElement) {
   let image = attractionData.images[0];
   let title = attractionData.name;
   let mrt = attractionData.mrt;
   if (mrt == null) {
      mrt = '無';
   }
   let category = attractionData.category;
   let id = attractionData.id;

   attractionElement.href = `attraction/${id}`;

   let attractionImage = document.createElement('div');
   attractionImage.classList.add('attraction-image');
   let imgElement = document.createElement('img');
   imgElement.src = image;

   attractionImage.appendChild(imgElement);
   attractionElement.appendChild(attractionImage);

   let titleElement = document.createElement('div');
   titleElement.classList.add('title');
   let titleContent = document.createTextNode(title);

   titleElement.appendChild(titleContent);
   attractionElement.appendChild(titleElement);            

   let mrtElement = document.createElement('div');
   mrtElement.classList.add('mrt');
   let mrtContent = document.createTextNode(mrt);

   mrtElement.appendChild(mrtContent);
   attractionElement.appendChild(mrtElement);            

   let categoryElement = document.createElement('div');
   categoryElement.classList.add('category');
   let categoryContent = document.createTextNode(category);

   categoryElement.appendChild(categoryContent);
   attractionElement.appendChild(categoryElement);    
}

function createNoResultElement() {
   let titleElement = document.createElement('div');
   titleElement.classList.add('no-result');
   const noResultConetent = document.createTextNode('沒有結果');

   titleElement.appendChild(noResultConetent);

   return titleElement;
}

// Infinite Scroll
window.addEventListener('scroll', debounce(infiniteScroll));

function debounce(func, wait = 100) {
   let timeout;
   return function() {
      const later = function() {
         clearTimeout(timeout);
         func();
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
   };
}

function infiniteScroll() {
   if (page == null) return;
   if (window.scrollY + window.innerHeight >= (document.body.scrollHeight - 200)) {
      if (!isFetching) {
         search();
      }
   }
}

