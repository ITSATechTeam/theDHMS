
// HANDLE FLASH MESSAGES ON DASHBOARD STARTS HERE
let flashGen = document.querySelector('.alert strong')
if(flashGen){
    console.log('flashGen around')
    setTimeout(() => {
        flashGen.style.display = 'none'
    }, 5000);
}
// HANDLE FLASH MESSAGES ON DASHBOARD ENDS HERE