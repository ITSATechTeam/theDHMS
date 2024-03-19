console.log('clicked')


// currentMonth DB SAVING FUNCTIONALITY STARTS HERE

let currentMonthName = document.querySelector('.currentMonth input').value
// FINDING VALUE OF CURRENT MONTH

const month = ["January","February","March","April","May","June","July","August","September","October","November","December"];
const newDate = new Date();
let currentMonth = month[newDate.getMonth()];
let previousMonth = month[newDate.getMonth() - 1];
console.log(currentMonth)
console.log(previousMonth)


currentMonthName = currentMonth

console.log(currentMonthName)


// currentMonth DB SAVING FUNCTIONALITY ENDS HERE


let maintenancereq = document.querySelector('.maintenancereq');
let requestmaintainbtn = document.querySelector('.requestmaintainbtn button');
let maintenancereqtopIMG = document.querySelector('.maintenancereqtop img');
const shadow = document.querySelector('.shadow2')


requestmaintainbtn.addEventListener('click', () => {
    shadow.style.display = 'block';
    maintenancereq.style.display = 'block';
})


maintenancereqtopIMG.addEventListener('click', () => {
    shadow.style.display = 'none';
    maintenancereq.style.display = 'none';
})

// REMOVING RANDOM NUMBER FROM DEVICE BRAND NAME STARTS HERE
let devicebrand = document.querySelector('.devicebrand').innerHTML
let devicebrand2 = document.querySelector('.devicebrand2')
console.log(devicebrand)

let devicebrandNew = []

devicebrandNew = devicebrand.split('·')
console.log(devicebrandNew[0])

devicebrand2.innerHTML = devicebrandNew[0]
// REMOVING RANDOM NUMBER FROM DEVICE BRAND NAME ENDS HERE



// SELECT SECTION TO DISPLAY: DEVICE DETAILS OF MAINTENANCE HISTORY DETAILS SETUP STARTS HERE
let devicedetailstoptab1Inner = document.querySelector('.devicedetailstoptab1Inner')
let AllmaintenanceRequests = document.querySelector('.AllmaintenanceRequests')
let deviceinfotab = document.querySelector('.deviceinfotab')
let maintainhistorytab = document.querySelector('.maintainhistorytab')
// activetab
deviceinfotab.classList.add('activetab')
maintainhistorytab.addEventListener('click', () => {
    maintainhistorytab.classList.add('activetab')
    deviceinfotab.classList.remove('activetab')
    devicedetailstoptab1Inner.style.display = 'none'
    AllmaintenanceRequests.style.display = 'block'
})

deviceinfotab.addEventListener('click', () => {
    deviceinfotab.classList.add('activetab')
    maintainhistorytab.classList.remove('activetab')
    AllmaintenanceRequests.style.display = 'none'
    devicedetailstoptab1Inner.style.display = 'block'
})


// SELECT SECTION TO DISPLAY: DEVICE DETAILS OF MAINTENANCE HISTORY DETAILS SETUP ENDS HERE


// HANDLE FLASH MESSAGES ON DASHBOARD STARTS HERE
let flashDevDetails = document.querySelector('#flash')
if(flashDevDetails){
    console.log('flashDevDetails around')
    setTimeout(() => {
        flashDevDetails.style.display = 'none'
    }, 5000);
}
// HANDLE FLASH MESSAGES ON DASHBOARD ENDS HERE