console.log('clicked')
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

