

// DISPLAY PAGINATION COUNT SELECTION SECTION STARTS HERE
// const selectedNumber = document.querySelector('.selectedNumber')
const selectedNumber = 5;
const selectPerPageCountBox = document.querySelector('.selectPerPageCountBox')
const selectPerPageCountBoxintro = document.querySelector('.selectPerPageCountBoxintro img')

// if(selectedNumber){
//     selectedNumber.addEventListener('click', () => {
//         selectPerPageCountBox.style.display = 'block'
//         shadow.style.display = 'block'
//     })
    
//     selectPerPageCountBoxintro.addEventListener('click', () => {
//         selectPerPageCountBox.style.display = 'none'
//         shadow.style.display = 'none'
//     })
// }

// DISPLAY PAGINATION COUNT SELECTION SECTION ENDS HERE


//PAGINATION STARTS HERE
const paginationNumbers = document.getElementById("pagination-numbers");
const paginatedList = document.getElementById("paginated-list");
const listItems = paginatedList.querySelectorAll(".item");
const nextButton = document.getElementById("next-button");
const prevButton = document.getElementById("prev-button");
const span = document.querySelector("span");
const numofitemsperpage = document.querySelector(".numofitemsperpage").value
// let selectedCount = document.querySelector(".selectedNumber p").innerHTML;
let selectedCount = 5
const pageNumberCount = document.querySelector(".pageNumberCount")
// 
const paginationLimit = selectedCount;


const pageCount = Math.ceil(listItems.length / paginationLimit);
pageNumberCount.innerHTML = pageCount
let currentPage = 1;
span.innerHTML = selectedCount;

const disableButton = (button) => {
  button.classList.add("disabled");
  button.setAttribute("disabled", true);
};

const enableButton = (button) => {
  button.classList.remove("disabled");
  button.removeAttribute("disabled");
};

const handlePageButtonsStatus = () => {
  if (currentPage === 1) {
    disableButton(prevButton);
  } else {
    enableButton(prevButton);
  }

  if (pageCount === currentPage) {
    disableButton(nextButton);
  } else {
    enableButton(nextButton);
  }
};

const handleActivePageNumber = () => {
  document.querySelectorAll(".pagination-number").forEach((button) => {
    button.classList.remove("active");
    const pageIndex = Number(button.getAttribute("page-index"));
    if (pageIndex == currentPage) {
      button.classList.add("active");
    //   console.log(pageIndex)
    }
  });
};

const appendPageNumber = (index) => {
  const pageNumber = document.createElement("button");
  pageNumber.className = "pagination-number";
  pageNumber.innerHTML = index;
  pageNumber.setAttribute("page-index", index);
  pageNumber.setAttribute("aria-label", "Page " + index);
    // const span = document.

  paginationNumbers.appendChild(pageNumber);
};

const getPaginationNumbers = () => {
  for (let i = 1; i <= pageCount; i++) {
    appendPageNumber(i);
  }
};

const setCurrentPage = (pageNum) => {
  currentPage = pageNum;

  handleActivePageNumber();
  handlePageButtonsStatus();
  
  const prevRange = (pageNum - 1) * paginationLimit;
  const currRange = pageNum * paginationLimit;

  listItems.forEach((item, index) => {
    item.classList.add("hidden");
    if (index >= prevRange && index < currRange) {
      item.classList.remove("hidden");
    }
  });
};

window.addEventListener("load", () => {
  getPaginationNumbers();
  setCurrentPage(1);

  prevButton.addEventListener("click", () => {
    setCurrentPage(currentPage - 1);
  });

  nextButton.addEventListener("click", () => {
    setCurrentPage(currentPage + 1);
  });

  document.querySelectorAll(".pagination-number").forEach((button) => {
    const pageIndex = Number(button.getAttribute("page-index"));

    if (pageIndex) {
      button.addEventListener("click", () => {
        setCurrentPage(pageIndex);
      });
    }
  });
});

//PAGINATION ENDS HERE

const shadoworg = document.querySelector('.shadoworg')

// let deviceherecountin = document.querySelector('.deviceherecountin')
// console.log(deviceherecountin)

// deviceherecountin.forEach((e)=>{
//     console.log(e)
//   })

let orgidentity = document.querySelectorAll('.substudentdevicecount')
orgidentity.forEach((e)=>{
    let elementCount = e.childElementCount
    e.innerHTML = elementCount
})


// DEVICE COUNT FOR ADMIN SECTION STARTS HERE
let subStudentCount = document.querySelectorAll('.substudentcount')
subStudentCount.forEach((e)=>{
    let elementCount = e.childElementCount
    e.innerHTML = elementCount
})


// DEVICE COUNT FOR ADMIN SECTION STARTS HERE
let adminDeviceCount = document.querySelectorAll('.devicescount')
adminDeviceCount.forEach((e)=>{
    let elementCount = e.childElementCount
    e.innerHTML = elementCount
})


let orgidentityStaffCount = document.querySelectorAll('.orgidentity')
orgidentityStaffCount.forEach((e)=>{
    let elementCount = e.nextElementSibling.nextElementSibling.nextElementSibling
    elementCount.innerHTML = elementCount.childElementCount
})


let AllActionbtns = document.querySelectorAll('.actionbtns')
AllActionbtns.forEach((e)=>{
    let AllActionbtnsCount = e.nextElementSibling
    e.addEventListener('click', () => {
        if (AllActionbtnsCount.style.display == 'block'){
            AllActionbtnsCount.style.display = 'none';
            // shadoworg.style.display = 'none';
        }else{
            AllActionbtnsCount.style.display = 'block';
            // shadoworg.style.display = 'block';
        }
    })
    // elementCount.innerHTML = elementCount.childElementCount
})



let actionbtnsmainin = document.querySelectorAll('.actionbtnsmainin')
actionbtnsmainin.forEach((e)=>{
    let elementCount = e.parentElement.nextElementSibling
    e.addEventListener('click', () => {
        shadoworg.style.display = 'block';
        elementCount.style.display = 'block'
        e.parentElement.style.display = 'none'
    })
})

let devicedetialsproperimg = document.querySelectorAll('.devicedetialsproper img')
let devicedetialsproper = document.querySelector('.devicedetialsproper')

devicedetialsproperimg.forEach((e)=>{
    let elementCount = e.parentElement
    e.addEventListener('click', () => {
        elementCount.style.display = 'none'
        shadoworg.style.display = 'none';
    })
})

