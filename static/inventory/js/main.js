// ADD DEVICE POPUP STARTS HERE
let addnewdevicebtn = document.querySelector('.addnewdevicebtn')
let registerDevice = document.querySelector('.registerDevice')
let shadow = document.querySelector('.shadow2')
let closeaddnewdeviceopoup = document.querySelector('.closeaddnewdeviceopoup')

addnewdevicebtn.addEventListener('click', () => {
    registerDevice.style.display = 'block'
    shadow.style.display = 'block'
})

closeaddnewdeviceopoup.addEventListener('click', () => {
    registerDevice.style.display = 'none'
    shadow.style.display = 'none'
})
// ADD DEVICE POPUP ENDS HERE

// UPLOAD CSV FILE STARTS POPUP HERE
let uploaddevicepopupintroclose = document.querySelector('.uploaddevicepopupintroclose')
let uploaddevicepopup = document.querySelector('.uploaddevicepopup')
let showdeviceuploadpopup = document.querySelector('.showdeviceuploadpopup')



showdeviceuploadpopup.addEventListener('click', () => {
    console.log('showdeviceuploadpopup clicked')
    uploaddevicepopup.style.display = 'block'
    shadow.style.display = 'block';
})


uploaddevicepopupintroclose.addEventListener('click', () => {
    uploaddevicepopup.style.display = 'none'
    shadow.style.display = 'none';
})
// UPLOAD CSV FILE ENDS POPUP HERE


// DISPLAY PAGINATION COUNT SELECTION SECTION STARTS HERE
const selectedNumber = document.querySelector('.selectedNumber')
const selectPerPageCountBox = document.querySelector('.selectPerPageCountBox')
const selectPerPageCountBoxintro = document.querySelector('.selectPerPageCountBoxintro img')

selectedNumber.addEventListener('click', () => {
    selectPerPageCountBox.style.display = 'block'
    shadow.style.display = 'block'
})

selectPerPageCountBoxintro.addEventListener('click', () => {
    selectPerPageCountBox.style.display = 'none'
    shadow.style.display = 'none'
})

// DISPLAY PAGINATION COUNT SELECTION SECTION ENDS HERE


//PAGINATION STARTS HERE
const paginationNumbers = document.getElementById("pagination-numbers");
const paginatedList = document.getElementById("paginated-list");
const listItems = paginatedList.querySelectorAll(".item");
const nextButton = document.getElementById("next-button");
const prevButton = document.getElementById("prev-button");
const span = document.querySelector("span");
const numofitemsperpage = document.querySelector(".numofitemsperpage").value
const selectedCount = document.querySelector(".selectedNumber p").innerHTML;
const pageNumberCount = document.querySelector(".pageNumberCount")
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

// FILTER BY CATEGORY STARTS HERE
const filtercategory = document.querySelector('.filtercategory')
const filtercalendar = document.querySelector('.filtercalendar')
// const shadow = document.querySelector('.shadow')
const filterbox1 = document.querySelector('.filterbox1')
const filterbox2 = document.querySelector('.filterbox2')
const closefilter = document.querySelector('.closefilter')
const closefilter2 = document.querySelector('.closefilter2')
const body = document.querySelector('.body')




filtercategory.addEventListener('click', () =>{
    shadow.style.display = 'block';
    filterbox1.style.display = 'block';
    // shadow.style.height === body.style.height
})

closefilter.addEventListener('click', () =>{
    shadow.style.display = 'none';
    filterbox1.style.display = 'none';

})

// FILTER BY CATEGORY ENDS HERE


// TABLE STARTS HERE
const topCheckBox = document.querySelector('.topCheckBox input')
const sectionCheckBox = document.querySelectorAll('.sectionCheckBox input')
if (topCheckBox.checked === true){
    sectionCheckBox.forEach(e => e.checked = true)
}else{
    sectionCheckBox.forEach(e => e.checked = false)
}


topCheckBox.addEventListener('change', () => {
    if (topCheckBox.checked === true){        sectionCheckBox.forEach(e => e.checked = true)
    }else{
        sectionCheckBox.forEach(e => e.checked = false)
    }
})
// TABLE ENDS HERE

// PREDELETE POP UP STARTS HERE

let allNodes = []
const testbox = document.querySelectorAll('.testbox')
testbox.text = 'Testing'
console.log(typeof(JSON.stringify(testbox)))
const testboxStr = JSON.stringify(testbox)
allNodes.push(testbox)
console.log(testbox)
console.log(allNodes)
console.log(testboxStr)

// allNodes.forEach(element => {
//   element.innerHTML = 'Testing'
// });


// for (var i in testbox) {
//   testbox[i].innerHTML = "Testing";
// }


const predelete = document.querySelector('.predelete')
const editDeviceData = document.querySelectorAll('.deleteDeviceData2')

for (var i in editDeviceData) {
  // editDeviceData[i].addEventListener('onmouseover', console.log('over it now'))
  editDeviceData[i].addEventListener('click', ('click', (e) => {
    e.preventDefault()
    predelete.style.display = 'block'
    shadow.style.display = 'block'
  }))
}


function loadDelPopUp (){
  editDeviceData.addEventListener('click', (e) => {
    e.preventDefault()
    predelete.style.display = 'block'
    shadow.style.display = 'block'
  })
}

// editDeviceData.addEventListener('click', () => {
//   predelete.style.display = 'block'
//   shadow.style.display = 'block'
// })


// PREDELETE POP UP ENDS HERE

