// console.log('working')
// let nav = document.querySelector('.nav')
// let outarrow = document.querySelector('.outsidebar')
// let navimages = document.querySelector('.navimages')
// let navlogo = document.querySelector('.navlogo')
// let outsidebar = document.querySelector('.outsidebar')
// let navlogout = document.querySelector('.navlogout')
// let topbar = document.querySelector('.topbar')
// // let mainbody = document.querySelector('.onboardbox')
// // mainbody.style.display = 'none'
// //
// let main = document.querySelector('.main')
// let hidesidebar = document.querySelector('.hidearrow')
// // .navshow

// outarrow.addEventListener('click', () => {
//     navimages.style.display = 'none'
//     outsidebar.style.display = 'none'
//     navlogo.style.display = 'none'
//     navlogout.style.display = 'none'
//     nav.classList.toggle('navhide')
//     // topbar.style.display = 'none'
//     topbar.style.marginLeft = '15%'
//     topbar.style.width = '85%'
//     // 
//     main.classList.toggle('navshow')
//     main.style.display = 'block'
// })

// hidesidebar.addEventListener('click', () =>{
//     navimages.style.display = 'block'
//     outsidebar.style.display = 'block'
//     navlogo.style.display = 'block'
//     navlogout.style.display = 'block'
//     nav.classList.toggle('navhide')
//     topbar.style.marginLeft = '5%'
//     topbar.style.width = '95%'
//     // 
//     main.classList.toggle('navshow')
//     setTimeout(() => {
//         main.style.display = 'none'
//     }, 00)
// })

// // MODILE TOP BAR DISPLAYA ND HIDE SETUP

// let downarrow = document.querySelector('.downarrow')
// let uparrow = document.querySelector('.uparrow')
// let searchandtools = document.querySelector('.searchandtools')

// downarrow.addEventListener('click', () => {
//     topbar.style.height = '200px'
//     downarrow.style.display='none'
//     uparrow.style.display='block'
//     setTimeout(() => {
//         searchandtools.style.display = 'block'
//     }, 500)
// })
// uparrow.addEventListener('click', () => {
//     topbar.style.height = '60px'
//     downarrow.style.display='block'
//     uparrow.style.display='none'
//     setTimeout(() => {
//         searchandtools.style.display = 'none'
//     }, 0)
// })



//   NOTIFICATION DISPLAY SIGN
let noticationSectionProper = document.querySelectorAll('.noticationSectionProper')
let CurrentNotificationAmount = Array.from(noticationSectionProper).length
let NewNotifyCount  = document.querySelector('.NewNotifyCount')
let NewNotifyCount2  = document.querySelector('.NewNotifyCount2')
NewNotifyCount.innerHTML = CurrentNotificationAmount
NewNotifyCount2.innerHTML = CurrentNotificationAmount

// console.log(CurrentNotificationAmount)


// PROFILE BOX DISPLAY SECTION STARTS HERE

const profileBox = document.querySelector('.profileBox')
const notifysectioninner = document.querySelector('.notifysectioninner')
const closereguser1 = document.querySelector('.closereguser1')

notifysectioninner.addEventListener('click', () => {
    profileBox.style.display = 'block'
    // console.log('clicked!')
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
let subadmin = document.querySelector('.subadmin')

let dashboardIcon = document.querySelector('#dashboardIcon')
let dashboardIconWhite = document.querySelector('#dashboardIconWhite')
dashboard.addEventListener('click', () => {
    dashboard.classList.add('active')
    dashboardIconWhite.style.display = 'block'
    dashboardIcon.style.display = 'none'
})
if (window.location.href.includes('dashboard')){
    dashboard.classList.add('active')
    dashboardIcon.style.fill='white'
}

// dashboard.addEventListener('mouseover', () => {
//     dashboardIcon.style.fill='white'
// })

// dashboard.addEventListener('mouseout', () => {
//     dashboardIcon.style.fill='#4F4F4F'
// })



let subadminIcon = document.querySelector('#subadminIcon')
if (window.location.href.includes('subadmin')){
    subadmin.classList.add('active')
    subadminIcon.style.fill='white'
}
// subadmin.addEventListener('mouseover', () => {
//     subadminIcon.style.fill='white'
// })
// subadmin.addEventListener('mouseout', () => {
//     subadminIcon.style.fill='#4F4F4F'
// })




let deviceInventoryIcon = document.querySelector('#deviceInventoryIcon')
if (window.location.href.includes('devicesinventory') || window.location.href.includes('editdevice') || window.location.href.includes('viewdevicedetails') ){
    dashboard.classList.remove('active')
    deviceinventory.classList.add('active')
    deviceInventoryIcon.style.fill='white'
}
// deviceinventory.addEventListener('mouseover', () => {
//     deviceInventoryIcon.style.fill='white'
// })
// deviceinventory.addEventListener('mouseout', () => {
//     deviceInventoryIcon.style.fill='#4F4F4F'
// })



let staffMemberIcon = document.querySelector('#staffMemberIcon')
let staffMemberIcon2 = document.querySelector('#staffMemberIcon2')
if (window.location.href.includes('staffmembers') || window.location.href.includes('staffdetails')){
    dashboard.classList.remove('active')
    deviceinventory.classList.remove('active')
    staffmembers.classList.add('active')

    staffMemberIcon.style.fill='white'
    staffMemberIcon2.style.fill='white'
}
// staffmembers.addEventListener('mouseover', () => {
//     staffMemberIcon.style.fill='white'
//     staffMemberIcon2.style.fill='white'
// })
// staffmembers.addEventListener('mouseout', () => {
//     staffMemberIcon.style.fill='#4F4F4F'
//     staffMemberIcon2.style.fill='#4F4F4F'
// })



let reportIcon = document.querySelector('#reportIcon')
if (window.location.href.includes('reports')){
    dashboard.classList.remove('active')
    deviceinventory.classList.remove('active')
    staffmembers.classList.remove('active')
    reports.classList.add('active')
    reportIcon.style.fill='white'
}
// reports.addEventListener('mouseover', () => {
//     reportIcon.style.fill='white'
// })
// reports.addEventListener('mouseout', () => {
//     reportIcon.style.fill='#4F4F4F'
// })



let supportIcon = document.querySelector('#supportIcon')
let supportIcon1 = document.querySelector('#supportIcon1')
if (window.location.href.includes('support')){
    dashboard.classList.remove('active')
    deviceinventory.classList.remove('active')
    staffmembers.classList.remove('active')
    reports.classList.remove('active')
    support.classList.add('active')
    supportIcon.style.fill='white'
    supportIcon1.style.fill='white'
}
// supportIcon supportIcon1
// support.addEventListener('mouseover', () => {
//     supportIcon.style.fill='white'
//     supportIcon1.style.fill='white'
// })
// support.addEventListener('mouseout', () => {
//     supportIcon.style.fill='#4F4F4F'
//     supportIcon1.style.fill='#4F4F4F'
// })



let maintenanceIcon = document.querySelector('#maintenanceIcon')
let maintenanceIcon1 = document.querySelector('#maintenanceIcon1')
if (window.location.href.includes('maintain') || window.location.href.includes('maintenancedetails') || window.location.href.includes('editmaintenancerequest')){
    dashboard.classList.remove('active')
    deviceinventory.classList.remove('active')
    staffmembers.classList.remove('active')
    support.classList.remove('active')
    reports.classList.remove('active')
    maintain.classList.add('active')
    maintenanceIcon.style.fill='white'
    maintenanceIcon1.style.fill='white'
}
// maintain.addEventListener('mouseover', () => {
//     maintenanceIcon.style.fill='white'
//     maintenanceIcon1.style.fill='white'
// })
// maintain.addEventListener('mouseout', () => {
//     maintenanceIcon.style.fill='#4F4F4F'
//     maintenanceIcon1.style.fill='#4F4F4F'
// })




let settingsIcon = document.querySelector('#settingsIcon')
if (window.location.href.includes('setting')){
    dashboard.classList.remove('active')
    deviceinventory.classList.remove('active')
    staffmembers.classList.remove('active')
    support.classList.remove('active')
    reports.classList.remove('active')
    maintain.classList.remove('active')
    settings.classList.add('active')
    settingsIcon.style.fill='white'
}
// settings.addEventListener('mouseover', () => {
//     settingsIcon.style.fill='white'
// })
// settings.addEventListener('mouseout', () => {
//     settingsIcon.style.fill='#4F4F4F'
// })



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
//     logout1.style.fill='white'
//     logout2.style.fill='white'
//     logout3.style.fill='white'
// })
// logout2




// PICK FIRST ALPHABET FROM USER NAME TO USE AS A DP STARTS HERE
let requestUser = document.querySelector('.requestUser').innerHTML
let profileimgsectiontext = document.querySelector('.profileimgsectiontext h1')
let profileimgsectiontext2 = document.querySelector('.profileimgsectiontext2 h1')
let firstAlphabet;
// console.log('requestUser')
for (let i = 0; i < requestUser.length; i++) {
    firstAlphabet = requestUser[0];
}

if(profileimgsectiontext){
    profileimgsectiontext.innerHTML = firstAlphabet
}
if(profileimgsectiontext2){
    profileimgsectiontext2.innerHTML = firstAlphabet
}


// PICK FIRST ALPHABET FROM USER NAME TO USE AS A DP ENDS HERE

// DISPLAY AND HIDE NOTIFICATION TAB
let desktopviewnotify = document.querySelector('.desktopviewnotify')
let mobileviewnotify = document.querySelector('.mobileviewnotify')
let allNotificationTabElements = document.querySelector('.allNotificationTabElements')
// desktopviewnotify.style.display = 'none'
desktopviewnotify.addEventListener('click', () => {
    if (allNotificationTabElements.style.display == 'block') {
        allNotificationTabElements.style.display = 'none'
    }else{
        allNotificationTabElements.style.display = 'block'
    }
})

mobileviewnotify.addEventListener('click', () => {
    if (allNotificationTabElements.style.display == 'block') {
        allNotificationTabElements.style.display = 'none'
    }else{
        allNotificationTabElements.style.display = 'block'
    }
})



// document.addEventListener("click", (e) => {
//     if (allNotificationTabElements.style.display = 'block') {
//         allNotificationTabElements.style.display = 'none'
//     }
//   });


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


// LOADING SCENE SETUP
var overlay = document.getElementById("overlay");

window.addEventListener('load', function(){
  overlay.style.display = 'none';
})




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











