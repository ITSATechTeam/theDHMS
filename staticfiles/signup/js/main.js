
// HANDLE FLASH MESSAGES ON DASHBOARD STARTS HERE
let flashSignup = document.querySelector('.alert strong')
if(flashSignup){
    console.log('flashSignup around')
    setTimeout(() => {
        flashSignup.style.display = 'none'
    }, 5000);
}
// HANDLE FLASH MESSAGES ON DASHBOARD ENDS HERE