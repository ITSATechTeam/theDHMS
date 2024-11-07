const eye = document.querySelector('.eye')
const eyeicon2 = document.querySelector('.eyeicon2')
const passwordInput = document.querySelector(".password")
// const passwordInput1 = document.querySelector(".password1")
if (eye){
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
}
// OTP PAGE ENTRY SETUP STARTS HERE
const otpeye = document.querySelector('.otpeye')
if(otpeye){
    const otpeyeicon2 = document.querySelector('.otpeyeicon2')
    const otppasswordInput = document.querySelector(".otppasswordInput")
    // const passwordInput1 = document.querySelector(".password1")
    
    otpeye.addEventListener("click", function(){
        this.classList.toggle("fa-eye-slash")
        const type = otppasswordInput.getAttribute("type") === "password" ? "text" : "password"
        otppasswordInput.setAttribute("type", type)
        otpeye.style.display = 'none'
        otpeyeicon2.style.display = 'block'
    })
    otpeyeicon2.addEventListener("click", function(){
        this.classList.toggle("fa-eye-slash")
        const type = otppasswordInput.getAttribute("type") === "password" ? "text" : "password"
        otppasswordInput.setAttribute("type", type)
        otpeye.style.display = 'block'
        otpeyeicon2.style.display = 'none'
    })
}

// OTP PAGE ENTRY SETUP ENDS HERE

// HANDLE FLASH MESSAGES ON DASHBOARD STARTS HERE
// let flashLogin = document.querySelector('.alert strong')
let flashLogin = document.querySelector('#flash')

if(flashLogin){
    console.log('flashLogin around')
    setTimeout(() => {
        flashLogin.style.display = 'none'
    }, 5000);
}
// HANDLE FLASH MESSAGES ON DASHBOARD ENDS HERE