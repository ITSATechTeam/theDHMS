// console.log('ooooo')
let addcommenttriggerbtn = document.querySelector('.addcommenttriggerbtn')
let addcommentproper = document.querySelector('.addcommentproper')
let addcommentcancel = document.querySelector('.addcommentcancel')


addcommenttriggerbtn.addEventListener('click', () => {
    addcommentproper.style.display = 'block'
})

addcommentcancel.addEventListener('click', () => {
    addcommentproper.style.display = 'none'
})