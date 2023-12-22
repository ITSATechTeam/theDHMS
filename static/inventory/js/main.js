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
let selectedCount = document.querySelector(".selectedNumber p").innerHTML;
const pageNumberCount = document.querySelector(".pageNumberCount")
// 

if (selectedCount === 'None'){
  selectedCount = '10'
}
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

// FILTER BY CATEGORY STARTS HERE
const filtercategory = document.querySelector('.filtercategory')
const filtercalendar = document.querySelector('.filtercalendar')
// const shadow = document.querySelector('.shadow')
const filterbox1 = document.querySelector('.filterbox1')
const filterbox2 = document.querySelector('.filterbox2')
const closefilter = document.querySelector('.closefilter')
const closefilter2 = document.querySelector('.closefilter2')
let filter2 = document.querySelector('.filter2')
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


filter2.addEventListener('click', () =>{
  console.log('filter2')
  shadow.style.display = 'block';
  filterbox2.style.display = 'block';
})


closefilter2.addEventListener('click', () =>{
  shadow.style.display = 'none';
  filterbox2.style.display = 'none';

})
// FILTER BY CATEGORY ENDS HERE


// TABLE GENERAL SELECTION SETUP STARTS HERE
const topCheckBox = document.querySelector('.topCheckBox input')
const sectionCheckBox = document.querySelectorAll('.sectionCheckBox input')
const numberofdevices = parseInt(document.querySelector('.numberofdevices h3').innerHTML)
// console.log(numberofdevices)


let detailsTabCountInnner = document.querySelector('.detailsTabCountInnner strong')
let detailsTabOut = document.querySelector('.detailsTabOut')
let detailsTabInnerEdit = document.querySelector('.detailsTabInnerEdit')
let detailsTabInnerViewDetails = document.querySelector('.detailsTabInnerViewDetails')
let selectedRequest = document.querySelector('.sectionCheckBox p')
let maintainName = document.querySelectorAll('.deviceID p')
let maintainNameID = document.getElementById('devicebrandName')
let maintainNameIDMain = document.querySelectorAll('.devicebrandName p')
maintainNameIDMain.forEach( (e)=>{
  // console.log(e.innerHTML)
} )
let maintainNameIDMain2= document.querySelectorAll('.maintainName i')
let ExportDataHere = document.querySelector('.ExportDataHere input')
let requesttoviewdetails = document.querySelector('.viewdetailsdetails input')

// DELETED AND EXPORT BUTTON FOR GENERAL AND NOT GENERAL SELECTIONS
let notSelectionDelete = document.querySelector('.notSelectionDelete')
let notSelectionExport = document.querySelector('.notSelectionExport')
// GENERALS BELOW
let generalSelectionDelete = document.querySelector('.generalSelectionDelete')
let generalSelectionExport = document.querySelector('.generalSelectionExport')


// ID SENDING SECTION STARTS HERE
let devicesID = document.querySelectorAll('.maintainName strong')
let sectionCheckID = document.querySelector('.sectionCheckID')
// console.log(devicesID)
let idforedit = document.querySelector('.idforedit input')
let deviceToDelete = document.querySelector('.deviceToDelete input')

// SELECT WHICH DELETE AND EXPORT BUTTONS TO DISPLAY DEPENDING ON THE NUMBER OF DEVICES SELECTED
topCheckBox.addEventListener('change', () => {
  if (topCheckBox.checked === true){
      console.log('topCheckBox is checked true now')
      notSelectionDelete.style.display = 'none'
      notSelectionExport.style.display = 'none'
      // 
      generalSelectionDelete.style.display = 'block';
      generalSelectionExport.style.display = 'block';
  }else{
      console.log('topCheckBox is NOT checked true now')
      notSelectionDelete.style.display = 'block'
      notSelectionExport.style.display = 'block'
      // 
      generalSelectionDelete.style.display = 'none';
      generalSelectionExport.style.display = 'none';
  }
})


if (topCheckBox.checked === true){
    sectionCheckBox.forEach(e => e.checked = true)
}else{
    sectionCheckBox.forEach(e => e.checked = false)
}


topCheckBox.addEventListener('change', () => {
    if (topCheckBox.checked === true){sectionCheckBox.forEach(e => e.checked = true)
    }else{
        sectionCheckBox.forEach(e => e.checked = false)
    }
})
// TABLE GENERAL SELECTION SETUP ENDS HERE


// CHECK BOX COUNTS SECTION STARTS HERE
let trueBoxes = 0;
let DataArray = []
let IDArray = []
function checkBoxFunctions(each){
    each.addEventListener('change', () => {
      console.log(each)
        maintainNameIDMain.forEach((e) => {
            let eValue = e.innerHTML
            if(eValue.includes(each.value)){
                DataArray.push(eValue);
                console.log(DataArray)
                return DataArray,
                ExportDataHere.value = DataArray,
                idforedit.value = DataArray, 
                deviceToDelete.value = DataArray,
                requesttoviewdetails.value = DataArray
            }
        })
        if (each.checked === true){
            trueBoxes += 1;
        }else{
            trueBoxes -= 1
        }
        detailsTabCountInnner.innerHTML = ` ${trueBoxes} `
        if (trueBoxes <= 0){
            trueBoxes = 0;
            detailsTabOut.style.display = 'none'
        }else{
            detailsTabOut.style.display = 'block'
        }
        if (trueBoxes > 1){
            detailsTabInnerEdit.style.display = 'none'
            detailsTabInnerViewDetails.style.display = 'none'
        }else if(trueBoxes <= 1){
            detailsTabInnerEdit.style.display = 'block'
            detailsTabInnerViewDetails.style.display = 'block'
        }
        
        if(trueBoxes < numberofdevices){
            topCheckBox.checked = false;
            console.log("all boxes are NOT checked 'true' now");
            generalSelectionDelete.style.display = 'none';
            generalSelectionExport.style.display = 'none';
        } else if (trueBoxes = numberofdevices){
            topCheckBox.checked = true;
            console.log("all boxes are checked 'true' now");
            notSelectionDelete.style.display = 'none'
            notSelectionExport.style.display = 'none'
            // 
            generalSelectionDelete.style.display = 'block';
            generalSelectionExport.style.display = 'block';
        }
    })
}

// EACH CHECKBOX SELECTION SETTINGS STARTS HERE
sectionCheckBox.forEach(each => {
    checkBoxFunctions(each)
})
// EACH CHECKBOX SELECTION SETTINGS ENDS HERE

// GENERAL SECTION EFFECT STARTS HERE
topCheckBox.addEventListener('change', () => {
  if (topCheckBox.checked === true){
          sectionCheckBox.forEach(e => {
              e.checked = true
              detailsTabCountInnner.innerHTML = `${numberofdevices} `
              trueBoxes = numberofdevices

              if (trueBoxes <= 0){
                  trueBoxes = 0;
                  detailsTabOut.style.display = 'none'
              }else{
                  detailsTabOut.style.display = 'block'
              }
              if (trueBoxes > 1){
                  detailsTabInnerEdit.style.display = 'none'
                  detailsTabInnerViewDetails.style.display = 'none'
              }else if(trueBoxes <= 1){
                  detailsTabInnerEdit.style.display = 'block'
                  detailsTabInnerViewDetails.style.display = 'block'
              }

          })
      
  }else{
      sectionCheckBox.forEach(e => {
          e.checked = false
          
          detailsTabCountInnner.innerHTML = `0 `
          trueBoxes = 0
          if (trueBoxes <= 0){
              trueBoxes = 0;
              detailsTabOut.style.display = 'none'
          }else{
              detailsTabOut.style.display = 'block'
          }
          if (trueBoxes > 1){
              detailsTabInnerEdit.style.display = 'none'
              detailsTabInnerViewDetails.style.display = 'none'
          }else if(trueBoxes <= 1){
              detailsTabInnerEdit.style.display = 'block'
              detailsTabInnerViewDetails.style.display = 'block'
          }
      })
  }
})
// GENERAL SECTION EFFECT ENDS HERE

// SET DEFAULT VALUE FOR DEVICES DISPLAY COUNT PER PAGE FUNCTIONALITY STARTS HERE
// let countperpage = document.querySelector('.selectedNumber p').innerHTML
// if (countperpage === 'None'){
//   countperpage = '10'
// }
// console.log(countperpage)

// SET DEFAULT VALUE FOR DEVICES DISPLAY COUNT PER PAGE FUNCTIONALITY ENDS HERE


// HANDLE FLASH MESSAGES ON DASHBOARD STARTS HERE
let flashGeneralInv = document.querySelector('#flashmessage')
// let flashGeneralInv = document.querySelector('.alert strong')
if(flashGeneralInv){
    setTimeout(() => {
        flashGeneralInv.style.display = 'none'
    }, 5000);
}
// HANDLE FLASH MESSAGES ON DASHBOARD ENDS HERE