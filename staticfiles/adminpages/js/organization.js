
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


let deviceslistpop = document.querySelector('.deviceslistpop')
let staffmemberspop = document.querySelector('.staffmemberspop')
let activitylogpop = document.querySelector('.activitylogpop')

let devinvetorg = document.querySelector('.devinvetorg')
let stafftableorg = document.querySelector('.stafftableorg')
let activitylogsection = document.querySelector('.activitylogsection')
// activeorgadminoptions

staffmemberspop.addEventListener('click', () => {
    devinvetorg.style.display = 'none'
    stafftableorg.style.display = 'block'
    activitylogsection.style.display = 'none'
    deviceslistpop.classList.remove('activeorgadminoptions')
    activitylogpop.classList.remove('activeorgadminoptions')
    staffmemberspop.classList.add('activeorgadminoptions')
})

activitylogpop.addEventListener('click', () => {
    devinvetorg.style.display = 'none'
    stafftableorg.style.display = 'none'
    activitylogsection.style.display = 'block'
    deviceslistpop.classList.remove('activeorgadminoptions')
    staffmemberspop.classList.remove('activeorgadminoptions')
    activitylogpop.classList.add('activeorgadminoptions')
})

deviceslistpop.addEventListener('click', () => {
    devinvetorg.style.display = 'block'
    stafftableorg.style.display = 'none'
    activitylogsection.style.display = 'none'
    deviceslistpop.classList.add('activeorgadminoptions')
    staffmemberspop.classList.remove('activeorgadminoptions')
    activitylogpop.classList.remove('activeorgadminoptions')
})

// 



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


let orgboxclosefilter = document.querySelector('.orgboxclosefilter')
let orgdetialsbox = document.querySelector('.orgdetialsbox')
let orgsectionintroinner = document.querySelector('.orgsectionintroinner img')


orgsectionintroinner.addEventListener('click', () => {
    shadoworg.style.display = 'block'
    orgdetialsbox.style.display = 'block'
})

orgboxclosefilter.addEventListener('click', () => {
    shadoworg.style.display = 'none'
    orgdetialsbox.style.display = 'none'
})
