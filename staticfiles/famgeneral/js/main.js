
//   NOTIFICATION DISPLAY SIGN
let noticationSectionProper = document.querySelectorAll('.noticationSectionProper')
let CurrentNotificationAmount = Array.from(noticationSectionProper).length
let NewNotifyCount  = document.querySelector('.NewNotifyCount')
NewNotifyCount.innerHTML = CurrentNotificationAmount

// console.log(CurrentNotificationAmount)


// PROFILE BOX DISPLAY SECTION STARTS HERE

const profileBox = document.querySelector('.profileBox')
const notifysectioninner = document.querySelector('.notifysectioninner')
const closereguser1 = document.querySelector('.closereguser1')

notifysectioninner.addEventListener('click', () => {
    profileBox.style.display = 'block'
    console.log('clicked!')
})


closereguser1.addEventListener('click', () => {
    profileBox.style.display = 'none'
})


// SIDEBAR ACTIVATIONS

let dashboard = document.querySelector('.dashboard')
let deviceinventory = document.querySelector('.deviceinventory')
let staffmembers = document.querySelector('.staffmembers')
let reports = document.querySelector('.reports')
let support = document.querySelector('.support')
let maintain = document.querySelector('.maintain')
let settings = document.querySelector('.settings')
let logout = document.querySelector('.logout')
let software = document.querySelector('.software')
// let subadmin = document.querySelector('.subadmin')

let dashboardIcon = document.querySelector('#dashboardIcon')
if (!window.location.href.includes('familyinventory') && !window.location.href.includes('familymember') && !window.location.href.includes('viewdevicedetails') ){
    dashboard.classList.add('active')
    dashboardIcon.style.fill='#2A66B0'
}


// if (window.location.href.includes('subadmin')){
//     subadmin.classList.add('active')
// }
// let subadminIcon = document.querySelector('#subadminIcon')
// subadmin.addEventListener('mouseover', () => {
//     subadminIcon.style.fill='#2A66B0'
// })
// subadmin.addEventListener('mouseout', () => {
//     subadminIcon.style.fill='#4F4F4F'
// })

let deviceInventoryIcon = document.querySelector('#deviceInventoryIcon')

if (window.location.href.includes('familyinventory') || window.location.href.includes('editdevice') || window.location.href.includes('viewdevicedetails') ){
    dashboard.classList.remove('active')
    deviceinventory.classList.add('active')
    deviceInventoryIcon.style.fill='#2A66B0'
}




let staffMemberIcon = document.querySelector('#staffMemberIcon')
let staffMemberIcon2 = document.querySelector('#staffMemberIcon2')
if (window.location.href.includes('familymember') || window.location.href.includes('staffdetails')){
    dashboard.classList.remove('active')
    deviceinventory.classList.remove('active')
    staffmembers.classList.add('active')
    staffMemberIcon.style.fill='#2A66B0'
    staffMemberIcon2.style.fill='#2A66B0'
}



let reportIcon = document.querySelector('#reportIcon')
if (window.location.href.includes('familyanalytics')){
    dashboard.classList.remove('active')
    deviceinventory.classList.remove('active')
    staffmembers.classList.remove('active')
    reports.classList.add('active')
    reportIcon.style.fill='#2A66B0'
    dashboardIcon.style.fill='#4F4F4F '
}



let supportIcon = document.querySelector('#supportIcon')
let supportIcon1 = document.querySelector('#supportIcon1')
if (window.location.href.includes('familysupport')){
    dashboard.classList.remove('active')
    deviceinventory.classList.remove('active')
    staffmembers.classList.remove('active')
    reports.classList.remove('active')
    support.classList.add('active')
    supportIcon.style.fill='#2A66B0'
    supportIcon1.style.fill='#2A66B0'
    dashboardIcon.style.fill='#4F4F4F '
}



let maintenanceIcon = document.querySelector('#maintenanceIcon')
let maintenanceIcon1 = document.querySelector('#maintenanceIcon1')
if (window.location.href.includes('familymaintain') || window.location.href.includes('maintenancedetails') || window.location.href.includes('editmaintenancerequest')){
    dashboard.classList.remove('active')
    deviceinventory.classList.remove('active')
    staffmembers.classList.remove('active')
    support.classList.remove('active')
    reports.classList.remove('active')
    maintain.classList.add('active')
    maintenanceIcon.style.fill='#2A66B0'
    maintenanceIcon1.style.fill='#2A66B0'
    dashboardIcon.style.fill='#4F4F4F '
}




let settingsIcon = document.querySelector('#settingsIcon')
if (window.location.href.includes('familysettings')){
    dashboard.classList.remove('active')
    deviceinventory.classList.remove('active')
    staffmembers.classList.remove('active')
    support.classList.remove('active')
    reports.classList.remove('active')
    maintain.classList.remove('active')
    settings.classList.add('active')
    settingsIcon.style.fill='#2A66B0'
    dashboardIcon.style.fill='#4F4F4F '
}



if (window.location.href.includes('software')){
    dashboard.classList.remove('active')
    deviceinventory.classList.remove('active')
    staffmembers.classList.remove('active')
    support.classList.remove('active')
    reports.classList.remove('active')
    maintain.classList.remove('active')
    settings.classList.remove('active')
    software.classList.add('active')
}

// let logout = document.querySelector('.logout2')

let logout1 = document.querySelector('#logout1')
let logout2 = document.querySelector('#logout2')
let logout3 = document.querySelector('#logout3')

// logout.addEventListener('mouseover', () => {
//     logout1.style.fill='#2A66B0'
//     logout2.style.fill='#2A66B0'
//     logout3.style.fill='#2A66B0'
// })
// logout2




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

// DISPLAY AND HIDE NOTIFICATION TAB
let notifyout = document.querySelector('.notifyout')
let allNotificationTabElements = document.querySelector('.allNotificationTabElements')

notifyout.addEventListener('mouseover', () => {
    allNotificationTabElements.style.display = 'block'
})


document.addEventListener("click", (e) => {
    if (allNotificationTabElements.style.display == 'block') {
        allNotificationTabElements.style.display = 'none'
    }
  });


// time for disappearing notifications
let alert = document.querySelector('.alert')
setTimeout(() => { clearInterval(alert); }, 5000); 


// HANDLE FLASH MESSAGES ON DASHBOARD STARTS HERE
let flashGeneral = document.querySelector('#flashmessage')
// let flashGeneral = document.querySelector('.alert strong')
if(flashGeneral){
    setTimeout(() => {
        flashGeneral.style.display = 'none'
    }, 5000);
}
// HANDLE FLASH MESSAGES ON DASHBOARD ENDS HERE













