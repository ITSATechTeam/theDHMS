const registerstaffbox = document.querySelector('.regsiteruser');
const addstaffbtn = document.querySelector('.addstaffbtn button');
const closereguser = document.querySelector('.closereguser');
const shadow1 = document.querySelector('.shadow1');

addstaffbtn.addEventListener('click', () => {
	registerstaffbox.style.display = 'block';
	shadow1.style.display = 'block';
})

closereguser.addEventListener('click', () => {
	registerstaffbox.style.display = 'none';
	shadow1.style.display = 'none';
})


// HANDLE FLASH MESSAGES ON DASHBOARD STARTS HERE
let flashStaff = document.querySelector('.alert strong')
if(flashStaff){
    console.log('flashStaff around')
    setTimeout(() => {
        flashStaff.style.display = 'none'
    }, 5000);
}
// HANDLE FLASH MESSAGES ON DASHBOARD ENDS HERE


// user online setup starts here

let userisonline = document.querySelector('.userisonline').innerHTML
let userisoffline = document.querySelector('.userisoffline')


if (userisonline != '' || userisonline){
    userisoffline.style.display = 'none'
}else{
    userisoffline.style.display = 'block'
}


// user online setup ends here