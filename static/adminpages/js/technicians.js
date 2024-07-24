let addTechnicianButton = document.querySelector('.addorgbtn1 button')
let addTechnicianButtonTwo = document.querySelector('.addorgbtn2')
let addTechnicianPopUp = document.querySelector('.regsiteruser')
let backgroundShadow = document.querySelector('.shadow1')
let popUpCloseButton = document.querySelector('.closereguser')

addTechnicianButton.addEventListener('click', () => {
        addTechnicianPopUp.style.display = 'block'
        backgroundShadow.style.display = 'block'
    }
)

if(addTechnicianButtonTwo){
    addTechnicianButtonTwo.addEventListener('click', () => {
            addTechnicianPopUp.style.display = 'block'
            backgroundShadow.style.display = 'block'
        }
    )

}


popUpCloseButton.addEventListener('click', () => {
        addTechnicianPopUp.style.display = 'none'
        backgroundShadow.style.display = 'none'
    }
)



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


// DISPLAY PAGINATION COUNT SELECTION SECTION STARTS HERE
// const selectedNumber = document.querySelector('.selectedNumber')
const selectedNumber = 10;
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

// window.addEventListener('click', () => {
//     AllActionbtns.forEach((e)=>{
//         let AllActionbtnsCount = e.nextElementSibling
//         e.addEventListener('click', () => {
//             if (AllActionbtnsCount.style.display == 'none'){
//                 AllActionbtnsCount.style.display = 'none';
//                 // shadoworg.style.display = 'none';
//             }else{
//                 AllActionbtnsCount.style.display = 'none';
//                 // shadoworg.style.display = 'none';
//             }
//         })
//         // elementCount.innerHTML = elementCount.childElementCount
//     })
// })
