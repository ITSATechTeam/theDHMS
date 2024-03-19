
// HANDLE FLASH MESSAGES ON DASHBOARD STARTS HERE
let flashGen = document.querySelector('#flash')
if(flashGen){
    console.log('flashGen around')
    setTimeout(() => {
        flashGen.style.display = 'none'
    }, 5000);
}
// HANDLE FLASH MESSAGES ON DASHBOARD ENDS HERE