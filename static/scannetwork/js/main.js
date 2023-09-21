console.log('working now')
const step1 = document.querySelector('.step1');
const step2 = document.querySelector('.step2');
const step3 = document.querySelector('.step3');
const step4 = document.querySelector('.step4');
const step5 = document.querySelector('.step5');
const step6 = document.querySelector('.step6');


const stage1 = document.querySelector('.stage1');
const stage2 = document.querySelector('.stage2');
const stage3 = document.querySelector('.stage3');
const stage4 = document.querySelector('.stage4');
const stage5 = document.querySelector('.stage5');
const stage6 = document.querySelector('.stage6');

const stepCount = document.querySelector('.stepCount span');
const upload = document.querySelector('.upload');


// STAGE ONE
step1.addEventListener('click',  () => {
    stage1.style.display = 'block';
    stage2.style.display = 'none';
    stage2.style.display = 'none';
    stage3.style.display = 'none';
    stage4.style.display = 'none';
    stage5.style.display = 'none';

    step1.classList.add('active')
    step2.classList.remove('active')
    step3.classList.remove('active')
    step4.classList.remove('active')
    step5.classList.remove('active')
    step6.classList.remove('active')
    stepCount.innerHTML = '1'
    next.style.display = 'block'
    upload.style.display = 'none'
})


// STAGE TWO
step2.addEventListener('click',  () => {
    stage1.style.display = 'none';
    step2.classList.add('active')
    stage2.style.display = 'none';
    stage3.style.display = 'none';
    stage4.style.display = 'none';
    stage5.style.display = 'none';

    step1.classList.remove('active')
    stage2.style.display = 'block';
    step3.classList.remove('active')
    step4.classList.remove('active')
    step5.classList.remove('active')
    step6.classList.remove('active')
    stepCount.innerHTML = '2'
    next.style.display = 'block'
    upload.style.display = 'none'
})


// STAGE THREE
step3.addEventListener('click',  () => {
    stage1.style.display = 'none';
    stage2.style.display = 'none';
    stage3.style.display = 'block';
    stage4.style.display = 'none';
    stage5.style.display = 'none';
    stage6.style.display = 'none';
    
    step1.classList.remove('active')
    step2.classList.remove('active')
    step3.classList.add('active')
    step4.classList.remove('active')
    step5.classList.remove('active')
    step6.classList.remove('active')
    stepCount.innerHTML = '3'
    next.style.display = 'block'
    upload.style.display = 'none'
})


// STAGE FOUR
step4.addEventListener('click',  () => {
    stage1.style.display = 'none';
    stage2.style.display = 'none';
    stage3.style.display = 'none';
    stage4.style.display = 'block';
    stage5.style.display = 'none';
    stage6.style.display = 'none';

    step1.classList.remove('active')
    step2.classList.remove('active')
    step3.classList.remove('active')
    step4.classList.add('active')
    step5.classList.remove('active')
    step6.classList.remove('active')
    stepCount.innerHTML = '4'
    next.style.display = 'block'
    upload.style.display = 'none'
})


// STAGE FIVE
step5.addEventListener('click',  () => {
    stage1.style.display = 'none';
    stage2.style.display = 'none';
    stage3.style.display = 'none';
    stage4.style.display = 'none';
    stage5.style.display = 'block';
    stage6.style.display = 'none';

    step1.classList.remove('active')
    step2.classList.remove('active')
    step3.classList.remove('active')
    step4.classList.remove('active')
    step5.classList.add('active')
    step6.classList.remove('active')
    stepCount.innerHTML = '5'
    next.style.display = 'block'
    upload.style.display = 'none'
})


// STAGE SIX
step6.addEventListener('click',  () => {
    stage1.style.display = 'none';
    stage2.style.display = 'none';
    stage3.style.display = 'none';
    stage4.style.display = 'none';
    stage5.style.display = 'none';
    stage6.style.display = 'block';

    step1.classList.remove('active')
    step2.classList.remove('active')
    step3.classList.remove('active')
    step4.classList.remove('active')
    step5.classList.remove('active')
    step6.classList.add('active')
    stepCount.innerHTML = '6'
    next.style.display = 'none'
    upload.style.display = 'block'

})


// NEXT AND PREVIOUS BUTTONS FUNCTIONALITY STARTS HERE

const previous = document.querySelector('.previous')
const next = document.querySelector('.next')
let displaying = 'stageTwo';

next.addEventListener('click', () => {
    if(displaying === 'stageTwo') {
        stage1.style.display = 'none';
        step2.classList.add('active')
        stage2.style.display = 'none';
        stage3.style.display = 'none';
        stage4.style.display = 'none';
        stage5.style.display = 'none';

        step1.classList.remove('active')
        stage2.style.display = 'block';
        step3.classList.remove('active')
        step4.classList.remove('active')
        step5.classList.remove('active')
        step6.classList.remove('active')
        stepCount.innerHTML = '2'
        displaying = 'stageThree'
    
    }else if(displaying === 'stageThree'){
        stage1.style.display = 'none';
        stage2.style.display = 'none';
        stage3.style.display = 'block';
        stage4.style.display = 'none';
        stage5.style.display = 'none';
        stage6.style.display = 'none';
        
        step1.classList.remove('active')
        step2.classList.remove('active')
        step3.classList.add('active')
        step4.classList.remove('active')
        step5.classList.remove('active')
        step6.classList.remove('active')
        stepCount.innerHTML = '3'
        displaying = 'stageFour'

    }else if(displaying === 'stageFour'){
        stage1.style.display = 'none';
        stage2.style.display = 'none';
        stage3.style.display = 'none';
        stage4.style.display = 'block';
        stage5.style.display = 'none';
        stage6.style.display = 'none';
    
        step1.classList.remove('active')
        step2.classList.remove('active')
        step3.classList.remove('active')
        step4.classList.add('active')
        step5.classList.remove('active')
        step6.classList.remove('active')
        stepCount.innerHTML = '4'
        displaying = 'stageFive'

    }else if(displaying === 'stageFive'){
        stage1.style.display = 'none';
        stage2.style.display = 'none';
        stage3.style.display = 'none';
        stage4.style.display = 'none';
        stage5.style.display = 'block';
        stage6.style.display = 'none';
    
        step1.classList.remove('active')
        step2.classList.remove('active')
        step3.classList.remove('active')
        step4.classList.remove('active')
        step5.classList.add('active')
        step6.classList.remove('active')
        stepCount.innerHTML = '5'
        displaying = 'stageSix'

    }else if(displaying === 'stageSix'){
        stage1.style.display = 'none';
        stage2.style.display = 'none';
        stage3.style.display = 'none';
        stage4.style.display = 'none';
        stage5.style.display = 'none';
        stage6.style.display = 'block';
    
        step1.classList.remove('active')
        step2.classList.remove('active')
        step3.classList.remove('active')
        step4.classList.remove('active')
        step5.classList.remove('active')
        step6.classList.add('active')
        stepCount.innerHTML = '6'
        displaying = 'stageOne'
        next.style.display = 'none'
        upload.style.display = 'block'

    }else if(displaying === 'stageOne'){
        stage1.style.display = 'block';
        stage2.style.display = 'none';
        stage2.style.display = 'none';
        stage3.style.display = 'none';
        stage4.style.display = 'none';
        stage5.style.display = 'none';
        stage6.style.display = 'none';
    
        step1.classList.add('active')
        step2.classList.remove('active')
        step3.classList.remove('active')
        step4.classList.remove('active')
        step5.classList.remove('active')
        step6.classList.remove('active')
        stepCount.innerHTML = '1'
        displaying = 'stageTwo'

    }
})

// PREVIOUS BUTTON EVENTS

previous.addEventListener('click', () => {
    
    next.style.display = 'block'
    upload.style.display = 'none'

    if(displaying === 'stageOne') {
        // console.log('No more previous to display')
        displaying = 'stageSix'
    }
    else if(displaying === 'stageTwo'){
        stage1.style.display = 'block';
        stage2.style.display = 'none';
        stage2.style.display = 'none';
        stage3.style.display = 'none';
        stage4.style.display = 'none';
        stage5.style.display = 'none';
    
        step1.classList.add('active')
        step2.classList.remove('active')
        step3.classList.remove('active')
        step4.classList.remove('active')
        step5.classList.remove('active')
        step6.classList.remove('active')
        stepCount.innerHTML = '1'
        displaying = 'stageOne'

    }else if(displaying === 'stageThree'){
        stage1.style.display = 'none';
        step2.classList.add('active')
        stage2.style.display = 'none';
        stage3.style.display = 'none';
        stage4.style.display = 'none';
        stage5.style.display = 'none';

        step1.classList.remove('active')
        stage2.style.display = 'block';
        step3.classList.remove('active')
        step4.classList.remove('active')
        step5.classList.remove('active')
        step6.classList.remove('active')
        stepCount.innerHTML = '2'
        displaying = 'stageTwo'

    }else if(displaying === 'stageFour'){
        stage1.style.display = 'none';
        stage2.style.display = 'none';
        stage3.style.display = 'block';
        stage4.style.display = 'none';
        stage5.style.display = 'none';
        stage6.style.display = 'none';
        
        step1.classList.remove('active')
        step2.classList.remove('active')
        step3.classList.add('active')
        step4.classList.remove('active')
        step5.classList.remove('active')
        step6.classList.remove('active')
        stepCount.innerHTML = '3'
        displaying = 'stageThree'
    }
   
    else if(displaying === 'stageFive'){
        stage1.style.display = 'none';
        stage2.style.display = 'none';
        stage3.style.display = 'none';
        stage4.style.display = 'block';
        stage5.style.display = 'none';
        stage6.style.display = 'none';
    
        step1.classList.remove('active')
        step2.classList.remove('active')
        step3.classList.remove('active')
        step4.classList.add('active')
        step5.classList.remove('active')
        step6.classList.remove('active')
        stepCount.innerHTML = '4'
        displaying = 'stageFour'

    }
    
    else if(displaying === 'stageSix'){
        stage1.style.display = 'none';
        stage2.style.display = 'none';
        stage3.style.display = 'none';
        stage4.style.display = 'none';
        stage5.style.display = 'block';
        stage6.style.display = 'none';
    
        step1.classList.remove('active')
        step2.classList.remove('active')
        step3.classList.remove('active')
        step4.classList.remove('active')
        step5.classList.add('active')
        step6.classList.remove('active')
        stepCount.innerHTML = '5'
        displaying = 'stageFive'
    }
})






// NEXT AND PREVIOUS BUTTONS FUNCTIONALITY ENDS HERE


// UPLOAD CSV FILE STARTS POPUP HERE
let uploaddevicepopupintroclose = document.querySelector('.uploaddevicepopupintroclose')
let uploaddevicepopup = document.querySelector('.uploaddevicepopup')
let showdeviceuploadpopup = document.querySelector('.showdeviceuploadpopup')
const shadow = document.querySelector('.shadow')



showdeviceuploadpopup.addEventListener('click', () => {
    console.log('showdeviceuploadpopup clicked')
    uploaddevicepopup.style.display = 'block'
    shadow.style.display = 'block';
})


uploaddevicepopupintroclose.addEventListener('click', () => {
    uploaddevicepopup.style.display = 'none'
    shadow.style.display = 'none';
})



// HANDLE FLASH MESSAGES ON DASHBOARD STARTS HERE
let flashScan = document.querySelector('.alert strong')
if(flashScan){
    console.log('flashScan around')
    setTimeout(() => {
        flashScan.style.display = 'none'
    }, 5000);
}
// HANDLE FLASH MESSAGES ON DASHBOARD ENDS HERE