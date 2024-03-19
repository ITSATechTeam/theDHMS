
// HANDLE FLASH MESSAGES ON DASHBOARD STARTS HERE
let flashEditDev = document.querySelector('#flash')
if(flashEditDev){
    console.log('flashEditDev around')
    setTimeout(() => {
        flashEditDev.style.display = 'none'
    }, 5000);
}
// HANDLE FLASH MESSAGES ON DASHBOARD ENDS HERE