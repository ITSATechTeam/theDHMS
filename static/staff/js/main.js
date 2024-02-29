const registerstaffbox = document.querySelector('.regsiteruser');
const addstaffbtn = document.querySelector('.addstaffbtn button');
const staffemptystatesectionbtn = document.querySelector('.staffemptystatesectionbtn button');
const closereguser = document.querySelector('.closereguser');
const shadow1 = document.querySelector('.shadow1');

addstaffbtn.addEventListener('click', () => {
	registerstaffbox.style.display = 'block';
	shadow1.style.display = 'block';
})

staffemptystatesectionbtn.addEventListener('click', () => {
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

let userisonline = document.querySelector('.userisonline')
if(userisonline){
    let userisonlineMain = userisonline.innerHTML
    let userisoffline = document.querySelector('.userisoffline')
    if (userisonlineMain != '' || userisonlineMain){
        userisoffline.style.display = 'none'
    }else{
        userisoffline.style.display = 'block'
    }
}



// user online setup ends here

let addstaffbtn2 = document.querySelector('.addstaffbtn2')
let ssopopupStageOne = document.querySelector('.ssopopupStageOne')
let ssopopupStageTwo = document.querySelector('.ssopopupStageTwo')
let shadowsso = document.querySelector('.shadowsso')
let ssopopupStageOneBTNNext = document.querySelector('.ssopopupStageOneBTNNext')
let ssopopupStageTwoBTNSPrevious = document.querySelector('.ssopopupStageTwoBTNSPrevious')
let ssopopupStageTwoBTNSNext = document.querySelector('.ssopopupStageTwoBTNSNext')
let uploaddevicepopupBTNPrev = document.querySelector('.uploaddevicepopupBTNPrev')
let uploaddevicepopup = document.querySelector('.uploaddevicepopup')
let uploaddevicepopupintroclose = document.querySelector('.uploaddevicepopupintroclose')

addstaffbtn2.addEventListener('click', () => {
    ssopopupStageOne.style.display = 'block'
    shadowsso.style.display = 'block'
})


ssopopupStageOneBTNNext.addEventListener('click', () => {
    ssopopupStageOne.style.display = 'none'
    ssopopupStageTwo.style.display = 'block'
    shadowsso.style.display = 'block'
})

ssopopupStageTwoBTNSPrevious.addEventListener('click', () => {
    ssopopupStageOne.style.display = 'block'
    ssopopupStageTwo.style.display = 'none'
    shadowsso.style.display = 'block'
})


uploaddevicepopupBTNPrev.addEventListener('click', () => {
    ssopopupStageOne.style.display = 'none'
    ssopopupStageTwo.style.display = 'block'
    uploaddevicepopup.style.display = 'none'
    shadowsso.style.display = 'block'

})

ssopopupStageTwoBTNSNext.addEventListener('click', () => {
    ssopopupStageOne.style.display = 'none'
    ssopopupStageTwo.style.display = 'none'
    uploaddevicepopup.style.display = 'block'
    shadowsso.style.display = 'block'
})

uploaddevicepopupintroclose.addEventListener('click', () => {
    ssopopupStageOne.style.display = 'none'
    ssopopupStageTwo.style.display = 'none'
    uploaddevicepopup.style.display = 'none'
    shadowsso.style.display = 'none'
})

let uploaddevicepopupintroclose2 = document.querySelector('.uploaddevicepopupintroclose2')
let uploaddevicepopupintroclose3 = document.querySelector('.uploaddevicepopupintroclose3')

uploaddevicepopupintroclose2.addEventListener('click', () => {
    ssopopupStageOne.style.display = 'none'
    ssopopupStageTwo.style.display = 'none'
    uploaddevicepopup.style.display = 'none'
    shadowsso.style.display = 'none'
})

uploaddevicepopupintroclose3.addEventListener('click', () => {
    ssopopupStageOne.style.display = 'none'
    ssopopupStageTwo.style.display = 'none'
    uploaddevicepopup.style.display = 'none'
    shadowsso.style.display = 'none'
})


