let hardwareNumber = document.querySelector('.hardwareNumber')
let hardwarePrices = document.querySelector('.hardwarePrices')

let NumberOfDevices = document.querySelector('.NumberOfDevices')
let AmountForDevices = document.querySelector('.AmountForDevices')

let selectElement = document.querySelector('#select1');
selectElement.addEventListener('click', () => {
  output = selectElement.value;
  if(output === 'NumberOfDevices'){
    hardwarePrices.style.display = 'none';
    hardwareNumber.style.display = 'block';
  }else{
    hardwarePrices.style.display = 'block';
    hardwareNumber.style.display = 'none';
  }
})



// HANDLE FLASH MESSAGES ON DASHBOARD STARTS HERE
let flashReport = document.querySelector('#flash')
if(flashReport){
    console.log('flashReport around')
    setTimeout(() => {
        flashReport.style.display = 'none'
    }, 5000);
}
// HANDLE FLASH MESSAGES ON DASHBOARD ENDS HERE