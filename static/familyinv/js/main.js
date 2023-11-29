let registerDeviceinv = document.querySelector('.registerDeviceinv')
let shadow = document.querySelector('.shadow')
let closeaddnewdeviceopoup = document.querySelector('.closeaddnewdeviceopoup')
let addnewdevicebtn = document.querySelector('.addnewdevicebtn button')
let emptystatebtn = document.querySelector('.emptystate button')


emptystatebtn.addEventListener('click', () => {
    shadow.style.display = 'block'
    registerDeviceinv.style.display = 'block'
})

addnewdevicebtn.addEventListener('click', () => {
    shadow.style.display = 'block'
    registerDeviceinv.style.display = 'block'
})

closeaddnewdeviceopoup.addEventListener('click', () => {
    shadow.style.display = 'none'
    registerDeviceinv.style.display = 'none'
})



