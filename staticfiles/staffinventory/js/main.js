
// HANDLE FLASH MESSAGES ON DASHBOARD STARTS HERE
let flashStaffInven = document.querySelector('.alert strong')
if(flashStaffInven){
    console.log('flashStaffInven around')
    setTimeout(() => {
        flashStaffInven.style.display = 'none'
    }, 5000);
}
// HANDLE FLASH MESSAGES ON DASHBOARD ENDS HERE