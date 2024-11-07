

// DISPLAY PAGINATION COUNT SELECTION SECTION STARTS HERE
// const selectedNumber = document.querySelector('.selectedNumber')
const selectedNumber = 5;
const selectPerPageCountBox = document.querySelector('.selectPerPageCountBox')
const selectPerPageCountBoxintro = document.querySelector('.selectPerPageCountBoxintro img')

// if(selectedNumber){
//     selectedNumber.addEventListener('click', () => {
//         selectPerPageCountBox.style.display = 'block'
//         shadow.style.display = 'block'
//     })
    
//     selectPerPageCountBoxintro.addEventListener('click', () => {
//         selectPerPageCountBox.style.display = 'none'
//         shadow.style.display = 'none'
//     })
// }

// DISPLAY PAGINATION COUNT SELECTION SECTION ENDS HERE

const shadoworg = document.querySelector('.shadoworg')

// let deviceherecountin = document.querySelector('.deviceherecountin')
// console.log(deviceherecountin)

// deviceherecountin.forEach((e)=>{
//     console.log(e)
//   })

let orgidentity = document.querySelectorAll('.orgidentity')


orgidentity.forEach((e)=>{
    let elementCount = e.nextElementSibling.nextElementSibling
    // console.log(elementCount.childElementCount)
    // console.log(elementCount)
    elementCount.innerHTML = elementCount.childElementCount
})


let orgidentityStaffCount = document.querySelectorAll('.orgidentity')
orgidentityStaffCount.forEach((e)=>{
    let elementCount = e.nextElementSibling.nextElementSibling.nextElementSibling
    elementCount.innerHTML = elementCount.childElementCount
})


let AllActionbtns = document.querySelectorAll('.actionbtns')
AllActionbtns.forEach((e)=>{
    let AllActionbtnsCount = e.nextElementSibling
    e.addEventListener('click', () => {
        if (AllActionbtnsCount.style.display == 'block'){
            AllActionbtnsCount.style.display = 'none';
            // shadoworg.style.display = 'none';
        }else{
            AllActionbtnsCount.style.display = 'block';
            // shadoworg.style.display = 'block';
        }
    })
    // elementCount.innerHTML = elementCount.childElementCount
})



let actionbtnsmainin = document.querySelectorAll('.actionbtnsmainin')
actionbtnsmainin.forEach((e)=>{
    let elementCount = e.parentElement.nextElementSibling
    e.addEventListener('click', () => {
        shadoworg.style.display = 'block';
        elementCount.style.display = 'block'
        e.parentElement.style.display = 'none'
    })
})

let devicedetialsproperimg = document.querySelectorAll('.devicedetialsproper img')
let devicedetialsproper = document.querySelector('.devicedetialsproper')

devicedetialsproperimg.forEach((e)=>{
    let elementCount = e.parentElement
    e.addEventListener('click', () => {
        elementCount.style.display = 'none'
        shadoworg.style.display = 'none';
    })
})

