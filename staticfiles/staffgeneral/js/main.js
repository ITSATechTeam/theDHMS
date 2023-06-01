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


if (window.location.href.includes('support')){
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

if (window.location.href.includes('setting')){
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


