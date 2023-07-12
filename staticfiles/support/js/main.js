let faqOne = document.querySelector('.faqOne')
let faqTwo = document.querySelector('.faqTwo')
let faqThree = document.querySelector('.faqThree')
let faqFour = document.querySelector('.faqFour')
let faqFive = document.querySelector('.faqFive')
let faqSix = document.querySelector('.faqSix')
let faqSeven = document.querySelector('.faqSeven')

// RESPONSE
let faqOneResponse = document.querySelector('.faqOneResponse')
let faqTwoResponse = document.querySelector('.faqTwoResponse')
let faqThreeResponse = document.querySelector('.faqThreeResponse')
let faqFourResponse = document.querySelector('.faqFourResponse')
let faqFiveResponse = document.querySelector('.faqFiveResponse')
let faqSixResponse = document.querySelector('.faqSixResponse')
let faqSevenResponse = document.querySelector('.faqSevenResponse')

// ALL ARROWS ARE BELOW

let showfaq1 = document.querySelector('.showfaq1')
let hidefaq1 = document.querySelector('.hidefaq1')
let showfaq2 = document.querySelector('.showfaq2')
let hidefaq2 = document.querySelector('.hidefaq2')
let showfaq3 = document.querySelector('.showfaq3')
let hidefaq3 = document.querySelector('.hidefaq3')
let showfaq4 = document.querySelector('.showfaq4')
let hidefaq4 = document.querySelector('.hidefaq4')
let showfaq5 = document.querySelector('.showfaq5')
let hidefaq5 = document.querySelector('.hidefaq5')
let showfaq6 = document.querySelector('.showfaq6')
let hidefaq6 = document.querySelector('.hidefaq6')
let showfaq7 = document.querySelector('.showfaq7')
let hidefaq7 = document.querySelector('.hidefaq7')

hidefaq1.style.display = 'none';
hidefaq2.style.display = 'none';
hidefaq3.style.display = 'none';
hidefaq4.style.display = 'none';
hidefaq5.style.display = 'none';
hidefaq6.style.display = 'none';
hidefaq7.style.display = 'none';


// faqTwoResponse.style.display = 'none';
faqOneResponse.style.display = 'none';
faqTwoResponse.style.display = 'none';
faqThreeResponse.style.display = 'none';
faqFourResponse.style.display = 'none';
faqFiveResponse.style.display = 'none';
faqSixResponse.style.display = 'none';
faqSevenResponse.style.display = 'none';
    
faqOne.addEventListener('click', () => {
    faqOneResponse.style.display = 'block';
    faqTwoResponse.style.display = 'none';
    faqThreeResponse.style.display = 'none';
    faqFourResponse.style.display = 'none';
    faqFiveResponse.style.display = 'none';
    faqSixResponse.style.display = 'none';
    faqSevenResponse.style.display = 'none';


    if(faqOneResponse.style.display === 'block'){
        showfaq1.style.display = 'none';
        showfaq2.style.display = 'block';
        showfaq3.style.display = 'block';
        showfaq4.style.display = 'block';
        showfaq5.style.display = 'block';
        showfaq6.style.display = 'block';
        showfaq7.style.display = 'block';
        // 
        hidefaq1.style.display = 'block';
        hidefaq2.style.display = 'none';
        hidefaq3.style.display = 'none';
        hidefaq4.style.display = 'none';
        hidefaq5.style.display = 'none';
        hidefaq6.style.display = 'none';
        hidefaq7.style.display = 'none';
    }
})





faqTwo.addEventListener('click', () => {
    faqOneResponse.style.display = 'none';
    faqTwoResponse.style.display = 'block';
    faqThreeResponse.style.display = 'none';
    faqFourResponse.style.display = 'none';
    faqFiveResponse.style.display = 'none';
    faqSixResponse.style.display = 'none';
    faqSevenResponse.style.display = 'none';
    showfaq2.style.display = 'none';
    hidefaq2.style.display = 'block';


    if(faqTwoResponse.style.display === 'block'){
        showfaq1.style.display = 'block';
        showfaq2.style.display = 'none';
        showfaq3.style.display = 'block';
        showfaq4.style.display = 'block';
        showfaq5.style.display = 'block';
        showfaq6.style.display = 'block';
        showfaq7.style.display = 'block';
        // 
        hidefaq1.style.display = 'none';
        hidefaq2.style.display = 'block';
        hidefaq3.style.display = 'none';
        hidefaq4.style.display = 'none';
        hidefaq5.style.display = 'none';
        hidefaq6.style.display = 'none';
        hidefaq7.style.display = 'none';
    }
})

faqThree.addEventListener('click', () => {
    faqOneResponse.style.display = 'none';
    faqTwoResponse.style.display = 'none';
    faqThreeResponse.style.display = 'block';
    faqFourResponse.style.display = 'none';
    faqFiveResponse.style.display = 'none';
    faqSixResponse.style.display = 'none';
    faqSevenResponse.style.display = 'none';
    if(faqThreeResponse.style.display === 'block'){
        showfaq1.style.display = 'block';
        showfaq2.style.display = 'block';
        showfaq3.style.display = 'none';
        showfaq4.style.display = 'block';
        showfaq5.style.display = 'block';
        showfaq6.style.display = 'block';
        showfaq7.style.display = 'block';
        // 
        hidefaq1.style.display = 'none';
        hidefaq2.style.display = 'none';
        hidefaq3.style.display = 'block';
        hidefaq4.style.display = 'none';
        hidefaq5.style.display = 'none';
        hidefaq6.style.display = 'none';
        hidefaq7.style.display = 'none';
    }
})

faqFour.addEventListener('click', () => {
    faqOneResponse.style.display = 'none';
    faqTwoResponse.style.display = 'none';
    faqThreeResponse.style.display = 'none';
    faqFourResponse.style.display = 'block';
    faqFiveResponse.style.display = 'none';
    faqSixResponse.style.display = 'none';
    faqSevenResponse.style.display = 'none';
    if(faqFourResponse.style.display === 'block'){
        showfaq1.style.display = 'block';
        showfaq2.style.display = 'block';
        showfaq3.style.display = 'block';
        showfaq4.style.display = 'none';
        showfaq5.style.display = 'block';
        showfaq6.style.display = 'block';
        showfaq7.style.display = 'block';
        // 
        hidefaq1.style.display = 'none';
        hidefaq2.style.display = 'none';
        hidefaq3.style.display = 'none';
        hidefaq4.style.display = 'block';
        hidefaq5.style.display = 'none';
        hidefaq6.style.display = 'none';
        hidefaq7.style.display = 'none';
    }
})

faqFive.addEventListener('click', () => {
    faqOneResponse.style.display = 'none';
    faqTwoResponse.style.display = 'none';
    faqThreeResponse.style.display = 'none';
    faqFourResponse.style.display = 'none';
    faqFiveResponse.style.display = 'block';
    faqSixResponse.style.display = 'none';
    faqSevenResponse.style.display = 'none';
    if(faqFiveResponse.style.display === 'block'){
        showfaq1.style.display = 'block';
        showfaq2.style.display = 'block';
        showfaq3.style.display = 'block';
        showfaq4.style.display = 'block';
        showfaq5.style.display = 'none';
        showfaq6.style.display = 'block';
        showfaq7.style.display = 'block';
        // 
        hidefaq1.style.display = 'none';
        hidefaq2.style.display = 'none';
        hidefaq3.style.display = 'none';
        hidefaq4.style.display = 'none';
        hidefaq5.style.display = 'block';
        hidefaq6.style.display = 'none';
        hidefaq7.style.display = 'none';
    }
})

faqSix.addEventListener('click', () => {
    faqOneResponse.style.display = 'none';
    faqTwoResponse.style.display = 'none';
    faqThreeResponse.style.display = 'none';
    faqFourResponse.style.display = 'none';
    faqFiveResponse.style.display = 'none';
    faqSixResponse.style.display = 'block';
    faqSevenResponse.style.display = 'none';
    if(faqSixResponse.style.display === 'block'){
        showfaq1.style.display = 'block';
        showfaq2.style.display = 'block';
        showfaq3.style.display = 'block';
        showfaq4.style.display = 'block';
        showfaq5.style.display = 'block';
        showfaq6.style.display = 'none';
        showfaq7.style.display = 'block';
        // 
        hidefaq1.style.display = 'none';
        hidefaq2.style.display = 'none';
        hidefaq3.style.display = 'none';
        hidefaq4.style.display = 'none';
        hidefaq5.style.display = 'none';
        hidefaq6.style.display = 'block';
        hidefaq7.style.display = 'none';
    }
})

faqSeven.addEventListener('click', () => {
    faqOneResponse.style.display = 'none';
    faqTwoResponse.style.display = 'none';
    faqThreeResponse.style.display = 'none';
    faqFourResponse.style.display = 'none';
    faqFiveResponse.style.display = 'none';
    faqSixResponse.style.display = 'none';
    faqSevenResponse.style.display = 'block';
    if(faqSevenResponse.style.display === 'block'){
        showfaq1.style.display = 'block';
        showfaq2.style.display = 'block';
        showfaq3.style.display = 'block';
        showfaq4.style.display = 'block';
        showfaq5.style.display = 'block';
        showfaq6.style.display = 'block';
        showfaq7.style.display = 'none';
        // 
        hidefaq1.style.display = 'none';
        hidefaq2.style.display = 'none';
        hidefaq3.style.display = 'none';
        hidefaq4.style.display = 'none';
        hidefaq5.style.display = 'none';
        hidefaq6.style.display = 'none';
        hidefaq7.style.display = 'block';
    }
})