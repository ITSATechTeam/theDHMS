// SIDEBAR ACTIVATIONS

let dashboard = document.querySelector('.dashboard')
let deviceinventory = document.querySelector('.deviceinventory')
// let staffmembers = document.querySelector('.staffmembers')
let reports = document.querySelector('.reports')
let support = document.querySelector('.support')
let maintain = document.querySelector('.maintain')
let settings = document.querySelector('.settings')
let logout = document.querySelector('.logout')
let software = document.querySelector('.software')

dashboard.addEventListener('click', () => {
    console.log('dashboard clicked')
    dashboard.classList.add('active')
})

if (window.location.href.includes('dashboard')){
    dashboard.classList.add('active')
}

if (window.location.href.includes('staffDeviceInventory') || window.location.href.includes('editdevice') || window.location.href.includes('viewdevicedetails') ){
    dashboard.classList.remove('active')
    deviceinventory.classList.add('active')
}

// if (window.location.href.includes('staffmembers') || window.location.href.includes('staffdetails')){
//     dashboard.classList.remove('active')
//     deviceinventory.classList.remove('active')
//     staffmembers.classList.add('active')
// }

if (window.location.href.includes('reports')){
    dashboard.classList.remove('active')
    deviceinventory.classList.remove('active')
    // staffmembers.classList.remove('active')
    reports.classList.add('active')
}


if (window.location.href.includes('staffsolution')){
    dashboard.classList.remove('active')
    deviceinventory.classList.remove('active')
    // staffmembers.classList.remove('active')
    // reports.classList.remove('active')
    support.classList.add('active')
}

if (window.location.href.includes('staffmaintenancerequests') || window.location.href.includes('staffmaintenancdetail') || window.location.href.includes('editmaintenancerequest')){
    dashboard.classList.remove('active')
    deviceinventory.classList.remove('active')
    // staffmembers.classList.remove('active')
    support.classList.remove('active')
    // reports.classList.remove('active')
    maintain.classList.add('active')
}

if (window.location.href.includes('staffsettings')){
    dashboard.classList.remove('active')
    deviceinventory.classList.remove('active')
    // staffmembers.classList.remove('active')
    support.classList.remove('active')
    // reports.classList.remove('active')
    maintain.classList.remove('active')
    settings.classList.add('active')
}


if (window.location.href.includes('software')){
    dashboard.classList.remove('active')
    deviceinventory.classList.remove('active')
    // staffmembers.classList.remove('active')
    support.classList.remove('active')
    reports.classList.remove('active')
    maintain.classList.remove('active')
    settings.classList.remove('active')
    software.classList.add('active')
}





// PICK FIRST ALPHABET FROM USER NAME TO USE AS A DP STARTS HERE
let requestUser = document.querySelector('.requestUser').innerHTML
let profileimgsectiontext = document.querySelector('.profileimgsectiontext h1')
let firstAlphabet;
// console.log('requestUser')
for (let i = 0; i < requestUser.length; i++) {
    firstAlphabet = requestUser[0];
}
profileimgsectiontext.innerHTML = firstAlphabet


// PICK FIRST ALPHABET FROM USER NAME TO USE AS A DP ENDS HERE


// PICK FIRST ALPHABET FROM USER NAME TO USE AS A DP STARTS HERE FOR MOBILE
let requestUser2 = document.querySelector('.requestUser').innerHTML
let profileimgsectiontext2 = document.querySelector('.profileimgsectiontext2 h1')
let firstAlphabet2;
// console.log('requestUser2')
for (let i = 0; i < requestUser2.length; i++) {
    firstAlphabet2 = requestUser2[0];
}
profileimgsectiontext2.innerHTML = firstAlphabet2

// PICK FIRST ALPHABET FROM USER NAME TO USE AS A DP ENDS HERE FOR MOBILE





// HANDLE FLASH MESSAGES ON DASHBOARD STARTS HERE
let flashStaffGeneral = document.querySelector('#flash')
if(flashStaffGeneral){
    console.log('flashStaffGeneral around')
    setTimeout(() => {
        flashStaffGeneral.style.display = 'none'
    }, 5000);
}
// HANDLE FLASH MESSAGES ON DASHBOARD ENDS HERE


// HAMBURGER MENU STARTS HERE
let hamburger = document.querySelector('.hamburger')

hamburger.addEventListener('click' , () => {
    hamburger.classList.toggle("hamburgeractive");
  });


let userSectionResponsiveOut = document.querySelector('.userSectionResponsiveOut')
let hamburgerMain = document.querySelector('.hamburgerMain')
let sidebarsection = document.querySelector('.sidebarsection')

hamburgerMain.addEventListener('click', () => {
    sidebarsection.classList.toggle('showMenu')
})
