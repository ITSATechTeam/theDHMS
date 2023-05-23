console.log('clicked')
let maintenancereq = document.querySelector('.maintenancereq');
let requestmaintainbtn = document.querySelector('.requestmaintainbtn button');
let maintenancereqtopIMG = document.querySelector('.maintenancereqtop img');


requestmaintainbtn.addEventListener('click', () => {
    maintenancereq.style.display = 'block';
})