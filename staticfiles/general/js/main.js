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

dashboard.addEventListener('click', () => {
    console.log('dashboard clicked')
    dashboard.classList.add('active')
})

if (window.location.href.includes('dashboard')){
    dashboard.classList.add('active')
}

if (window.location.href.includes('devicesinventory')){
    dashboard.classList.remove('active')
    deviceinventory.classList.add('active')
}

if (window.location.href.includes('staffmembers')){
    dashboard.classList.remove('active')
    deviceinventory.classList.remove('active')
    staffmembers.classList.add('active')
}

if (window.location.href.includes('reports')){
    dashboard.classList.remove('active')
    deviceinventory.classList.remove('active')
    staffmembers.classList.remove('active')
    reports.classList.add('active')
}


if (window.location.href.includes('support')){
    dashboard.classList.remove('active')
    deviceinventory.classList.remove('active')
    staffmembers.classList.remove('active')
    reports.classList.remove('active')
    support.classList.add('active')
}

if (window.location.href.includes('maintain')){
    dashboard.classList.remove('active')
    deviceinventory.classList.remove('active')
    staffmembers.classList.remove('active')
    support.classList.remove('active')
    reports.classList.remove('active')
    maintain.classList.add('active')
}

if (window.location.href.includes('setting')){
    dashboard.classList.remove('active')
    deviceinventory.classList.remove('active')
    staffmembers.classList.remove('active')
    support.classList.remove('active')
    reports.classList.remove('active')
    maintain.classList.remove('active')
    settings.classList.add('active')
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


