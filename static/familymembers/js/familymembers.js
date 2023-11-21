
let familymemberintrobtn = document.querySelector('.familymemberintrobtn button')
let addfampopup = document.querySelector('.addfampopup')
let shadow = document.querySelector('.shadow')
let addfampopupheadclosebtn = document.querySelector('.addfampopupheadclosebtn')

familymemberintrobtn.addEventListener('click', () => {
    addfampopup.style.display = 'block'
    shadow.style.display = 'block'
})

addfampopupheadclosebtn.addEventListener('click', () => {
    addfampopup.style.display = 'none'
    shadow.style.display = 'none'
})

// HANDLE FLASH MESSAGES ON FAMILY MEMBER AREA STARTS HERE
let flashfammember = document.querySelector('.alert')
// let flashGeneral = document.querySelector('.alert strong')
if (flashfammember){
    setInterval(() => {
        flashfammember.style.display = 'none'
    }, 5000);
}
// HANDLE FLASH MESSAGES ON FAMILY MEMBER AREA ENDS HERE

// NO FAMILY MEMBER YET SETUP STARTS HERE
let familymemberCount = document.querySelector('.familymemberCount p').innerHTML
let mainfamilymemberslistsection = document.querySelector('.mainfamilymemberslistsection')
let emptystate = document.querySelector('.emptystate')


if (familymemberCount === '0'){
    mainfamilymemberslistsection.style.display = 'none'
    emptystate.style.display = 'block'
}else{
    mainfamilymemberslistsection.style.display = 'block'
    emptystate.style.display = 'none'
}






