
// NO SUB ADMIN YET SETUP STARTS HERE
let NumberOfSubAdmin = document.querySelector('.maintainRequestCount p').innerHTML
let AboveOneSubAdmin = document.querySelector('.midSearchSubadminSection')
let table = document.querySelector('.table')
let NoSubAdminDisplay = document.querySelector('.addSubadminMain')

if (NumberOfSubAdmin === '0'){
    AboveOneSubAdmin.style.display = 'none'
    table.style.display = 'none'
    NoSubAdminDisplay.style.display = 'block'
}





let AllSelectedSubAdmin = []
let allSubAdminArrForm = document.querySelector('.allSubAdminArrForm')
let allSubAdminArr = document.querySelector('.allSubAdmin')
let addSubAdminPopUpList = document.getElementsByClassName('addSubAdminPopUpList')

for(let subAdmin of addSubAdminPopUpList){
    let subAdminRadio = subAdmin.lastChild.previousSibling
    subAdmin.addEventListener('click', () => {
        subAdminRadio.checked = true
        AllSelectedSubAdmin.push(subAdminRadio.value)
        subAdmin.classList.add('changeBckgdColor')
    })
}


allSubAdminArrForm.addEventListener('submit', () => {
    console.log('form submitted')
    allSubAdminArr.value = AllSelectedSubAdmin
})


allSubAdminArr.value = AllSelectedSubAdmin



// REVEAL SUB ADMIN POP UP TAB

let addSubadminMainBTN = document.querySelector('.addSubadminMainBTN')
let scannetworkbtn = document.querySelector('.scannetworkbtnBTNMain')
let addSubAdminPopUp = document.querySelector('.addSubAdminPopUp')
let shadowSubAdmin = document.querySelector('.shadowSubAdmin')
let addSubAdminPopUpClose = document.querySelector('.addSubAdminPopUpClose')


scannetworkbtn.addEventListener('click', () => {
    addSubAdminPopUp.style.display = 'block';
    shadowSubAdmin.style.display = 'block';
})


addSubadminMainBTN.addEventListener('click', () => {
    addSubAdminPopUp.style.display = 'block';
    shadowSubAdmin.style.display = 'block';
})

addSubAdminPopUpClose.addEventListener('click', () => {
    addSubAdminPopUp.style.display = 'none';
    shadowSubAdmin.style.display = 'none';
})

// DISPLAY ERROR POPUP
// A staff you selected already exists. Please select a non Sub-Admin to assign.

let errordisplay = document.querySelector('.errordisplay').innerHTML
let errorSubAdminTab = document.querySelector('.errorSubAdminTab')
let errorSubAdminTab2 = document.querySelector('.errorSubAdminTab2')
let errorSubAdminTab3 = document.querySelector('.errorSubAdminTab3')
let addErrorPopUpClose = document.querySelector('.addErrorPopUpClose')


console.log(errordisplay)
if (errordisplay === 'A staff you selected already exists as a sub-Admin. Please select a non Sub-Admin to assign.'){
    errorSubAdminTab.style.display = 'block'
    shadowSubAdmin.style.display = 'block';
}

addErrorPopUpClose.addEventListener('click', () => {
    errorSubAdminTab.style.display = 'none'
    shadowSubAdmin.style.display = 'none';
})

if (errordisplay === 'You selected two staff members from the same department. Please select one staff member per department.'){
    errorSubAdminTab2.style.display = 'block'
    shadowSubAdmin.style.display = 'block';
}



// You selected a staff whose department already has a subadmin, please delete existing subadmin before reassigning..

if (errordisplay === 'You selected a staff whose department already has a subadmin, please delete existing subadmin before reassigning.'){
    errorSubAdminTab3.style.display = 'block'
    shadowSubAdmin.style.display = 'block';
}





// HANDLE FLASH MESSAGES ON DASHBOARD STARTS HERE
let flashSubdomain = document.querySelector('#flash')
if(flashSubdomain){
    console.log('flashSubdomain around')
    setTimeout(() => {
        flashSubdomain.style.display = 'none'
    }, 5000);
}
// HANDLE FLASH MESSAGES ON DASHBOARD ENDS HERE