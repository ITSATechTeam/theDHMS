const eye = document.querySelector('.eye')
const eyeicon2 = document.querySelector('.eyeicon2')
const passwordInput = document.querySelector(".password")
const passwordstrengthcheckfull = document.querySelector('.passwordstrengthcheck')
// const passwordInput1 = document.querySelector(".password1")

eye.addEventListener("click", function(){
    this.classList.toggle("fa-eye-slash")
    const type = passwordInput.getAttribute("type") === "password" ? "text" : "password"
    passwordInput.setAttribute("type", type)
    eye.style.display = 'none'
    eyeicon2.style.display = 'block'
})

eyeicon2.addEventListener("click", function(){
    this.classList.toggle("fa-eye-slash")
    const type = passwordInput.getAttribute("type") === "password" ? "text" : "password"
    passwordInput.setAttribute("type", type)
    eye.style.display = 'block'
    eyeicon2.style.display = 'none'
})


// HANDLE FLASH MESSAGES ON DASHBOARD STARTS HERE
let flashLogin = document.querySelector('#flash')
if(flashLogin){
    console.log('flashLogin around')
    setTimeout(() => {
        flashLogin.style.display = 'none'
    }, 5000);
}
// HANDLE FLASH MESSAGES ON DASHBOARD ENDS HERE


// performs password checks functionlity starts here
let checklenght = document.querySelector('.checklenght img')
let checkcase = document.querySelector('.checkcase img')
let checknum = document.querySelector('.checknum img')
let checkspec = document.querySelector('.checkspec img')
let submitformbtn = document.querySelector('.submitformbtn')
let submitbtnbeforechecks = document.querySelector('.submitbtnbeforechecks')



const passwordInput2 = document.querySelector(".password")
const specialChars = /[`!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;
let checklenghtRate, checkcaseRate, specialCharsRate, checknumRate;
setInterval(() => {
    let passwordtotext = passwordInput.value
    if(passwordtotext.length >= 8){
        checklenght.style.backgroundColor = '#2A66B0'
        checklenghtRate = 25;
    }else{        
        checklenght.style.backgroundColor = 'transparent'
        checklenghtRate = 0;
    }
    if(passwordtotext.match(/[A-Z]/)){
        checkcase.style.backgroundColor = '#2A66B0'
        checkcaseRate = 25;
    }else{        
        checkcase.style.backgroundColor = 'transparent'
        checkcaseRate = 0;
    }
    if (specialChars.test(passwordtotext)){
        checkspec.style.backgroundColor = '#2A66B0'
        specialCharsRate = 25;
    }else{        
        checkspec.style.backgroundColor = 'transparent'
        specialCharsRate = 0;
    }
    if(/[0-9]/.test(passwordtotext)){
        checknum.style.backgroundColor = '#2A66B0'
        checknumRate = 25;
    }else{        
        checknum.style.backgroundColor = 'transparent'
        checknumRate = 0;
    }
    if(passwordtotext.length >= 8 && passwordtotext.match(/[A-Z]/) && specialChars.test(passwordtotext) && /[0-9]/.test(passwordtotext)){
        submitformbtn.style.display = 'block'
    }else{
        submitformbtn.style.display = 'none'
    }
    
    let strenghtRate = checklenghtRate + checkcaseRate + specialCharsRate + checknumRate;
    // passwordstrengthcheckfull.innerHTML = `Your Password is ${strenghtRate}% strong`
    if(strenghtRate == 100){
        passwordstrengthcheckfull.innerHTML = `Welldone👍! Your password strenght is ${strenghtRate}%. Please click the sign up button to continue.`
    }else if(strenghtRate == 0) {
        passwordstrengthcheckfull.innerHTML = `😩Your Password is ${strenghtRate}% strong`
    }else if(strenghtRate == 25) {
        passwordstrengthcheckfull.innerHTML = `😊Your Password is ${strenghtRate}% strong.`
    }else if(strenghtRate == 50) {
        passwordstrengthcheckfull.innerHTML = `😒Your Password is ${strenghtRate}% strong. Half way to go!`
    }else if(strenghtRate == 75) {
        passwordstrengthcheckfull.innerHTML = `😊Your Password is ${strenghtRate}% strong. You're almost there!`
    }
}, 1000);





// HANDLE FLASH MESSAGES ON DASHBOARD STARTS HERE
let companyflashmessage = document.querySelector('#flashmessage')
// let companyflashmessage = document.querySelector('.alert strong')
if(companyflashmessage){
    setTimeout(() => {
        companyflashmessage.style.display = 'none'
    }, 5000);
}



// Validate input filed for text
const companynameinput = document.querySelector('.companyname');
companynameinput.addEventListener('keydown', function(event){
  if((/\d/g).test(event.key)) event.preventDefault();
})


















