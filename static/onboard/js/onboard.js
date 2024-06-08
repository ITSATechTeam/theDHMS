const eye = document.querySelector('.eye')
const eyeicon2 = document.querySelector('.eyeicon2')
const passwordInput = document.querySelector(".password")
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
setInterval(() => {
    let passwordtotext = passwordInput.value
    if(passwordtotext.length >= 8){
        checklenght.style.backgroundColor = '#2A66B0'
    }else{        
        checklenght.style.backgroundColor = 'transparent'
    }
    if(passwordtotext.match(/[A-Z]/)){
        checkcase.style.backgroundColor = '#2A66B0'
    }else{        
        checkcase.style.backgroundColor = 'transparent'
    }
    if (specialChars.test(passwordtotext)){
        checkspec.style.backgroundColor = '#2A66B0'
    }else{        
        checkspec.style.backgroundColor = 'transparent'
    }
    if(/[0-9]/.test(passwordtotext)){
        checknum.style.backgroundColor = '#2A66B0'
    }else{        
        checknum.style.backgroundColor = 'transparent'
    }
    if(passwordtotext.length >= 8 && passwordtotext.match(/[A-Z]/) && specialChars.test(passwordtotext) && /[0-9]/.test(passwordtotext)){
        submitformbtn.style.display = 'block'
        submitbtnbeforechecks.style.display = 'none'
    }else{
        submitformbtn.style.display = 'none'
        submitbtnbeforechecks.style.display = 'block'
    }
}, 1000);




// HANDLE FLASH MESSAGES ON DASHBOARD STARTS HERE
let flashfamilyonboard = document.querySelector('#flashmessage')
// let flashfamilyonboard = document.querySelector('.alert strong')
if(flashfamilyonboard){
    setTimeout(() => {
        flashfamilyonboard.style.display = 'none'
    }, 5000);
}


// Validate input filed for text
const fullnameinput = document.querySelector('#fullname');
fullnameinput.addEventListener('keydown', function(event){
  if((/\d/g).test(event.key)) event.preventDefault();
})






















