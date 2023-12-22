

let requestmain = document.querySelector('.requestmain')
let requestmaintenance = document.querySelector('.requestmaintenance')
let requestmainclosebtn = document.querySelector('.requestmainclosebtn')
let shadow = document.querySelector('.shadow')


requestmaintenance.addEventListener('click', () => {
    requestmain.style.display = 'block';
    shadow.style.display = 'block';
})

requestmainclosebtn.addEventListener('click', () => {
    requestmain.style.display = 'none';
    shadow.style.display = 'none';
})







