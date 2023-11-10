console.log('running')
// const filtercategory = document.querySelector('.filtercategory')
// const shadow = document.querySelector('.shadow2')
// const closefilter = document.querySelector('.closefilter')
// const closefilter2 = document.querySelector('.closefilter2')
// let filter2 = document.querySelector('.filter2')
// const filterbox1 = document.querySelector('.filterbox1')
// const filterbox2 = document.querySelector('.filterbox2')


// filtercategory.addEventListener('click', () =>{
//     shadow.style.display = 'block';
//     filterbox1.style.display = 'block';
//     // shadow.style.height === body.style.height
// })

// closefilter.addEventListener('click', () =>{
//     shadow.style.display = 'none';
//     filterbox1.style.display = 'none';

// })

// filter2.addEventListener('click', () =>{
//     console.log('filter2')
//     shadow.style.display = 'block';
//     filterbox2.style.display = 'block';
// })


// closefilter2.addEventListener('click', () =>{
//     shadow.style.display = 'none';
//     filterbox2.style.display = 'none';

// })



// // HANDLE FLASH MESSAGES ON DASHBOARD STARTS HERE
// let flashStaffDash = document.querySelector('.alert strong')
// if(flashStaffDash){
//     console.log('flashStaffDash around')
//     setTimeout(() => {
//         flashStaffDash.style.display = 'none'
//     }, 5000);
// }
// HANDLE FLASH MESSAGES ON DASHBOARD ENDS HERE

let existingUserName = document.querySelector('.existingUserName').innerHTML
console.log(existingUserName)
let shadowforazurepopup = document.querySelector('.shadowforazurepopup')
if (existingUserName === 'NoUser'){
    shadowforazurepopup.style.display = 'block'
}else{    
    shadowforazurepopup.style.display = 'none'
}
