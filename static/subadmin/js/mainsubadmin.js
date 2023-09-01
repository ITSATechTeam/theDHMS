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
let scannetworkbtn = document.querySelector('.scannetworkbtnBTNMain')
let addSubAdminPopUp = document.querySelector('.addSubAdminPopUp')
let shadowSubAdmin = document.querySelector('.shadowSubAdmin')
let addSubAdminPopUpClose = document.querySelector('.addSubAdminPopUpClose')


scannetworkbtn.addEventListener('click', () => {
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
let addErrorPopUpClose = document.querySelector('.addErrorPopUpClose')


console.log(errordisplay)
if (errordisplay === 'A staff you selected already exists. Please select a non Sub-Admin to assign.'){
    errorSubAdminTab.style.display = 'block'
    shadowSubAdmin.style.display = 'block';
}

addErrorPopUpClose.addEventListener('click', () => {
    errorSubAdminTab.style.display = 'none'
    shadowSubAdmin.style.display = 'none';
})








