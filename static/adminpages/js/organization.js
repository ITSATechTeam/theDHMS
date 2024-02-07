

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
    // console.log(elementCount.childElementCount)
    // console.log(elementCount)
    elementCount.innerHTML = elementCount.childElementCount
})







