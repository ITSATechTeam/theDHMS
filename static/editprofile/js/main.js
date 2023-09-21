const eye = document.querySelector('.eye')
const eye1 = document.querySelector('.eye1')
const eyeicon2 = document.querySelector('.eyeicon2')
const eyeicon3 = document.querySelector('.eyeicon3')
const passwordInput = document.querySelector(".password")
const passwordInput1 = document.querySelector(".password1")

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



eye1.addEventListener("click", function(){
    this.classList.toggle("fa-eye-slash")
    const type = passwordInput1.getAttribute("type") === "password" ? "text" : "password"
    passwordInput1.setAttribute("type", type)
    eye1.style.display = 'none'
    eyeicon3.style.display = 'block'
  })

eyeicon3.addEventListener("click", function(){
    this.classList.toggle("fa-eye-slash")
    const type = passwordInput1.getAttribute("type") === "password" ? "text" : "password"
    passwordInput1.setAttribute("type", type)
    eye1.style.display = 'block'
    eyeicon3.style.display = 'none'
  })



  // PROFILE IMAGE UPLOAD DETECTION STARTS HERE
let profilepicture = document.querySelector('.profilepicture')
let formsubmitbtn = document.querySelector('.formsubmitbtn')
  if(profilepicture.value != "") {
    console.log("profilepicture")
    formsubmitbtn.style.display = 'block'
 }



// HANDLE FLASH MESSAGES ON DASHBOARD STARTS HERE
let flashEditProfile = document.querySelector('.alert strong')
if(flashEditProfile){
    console.log('flashEditProfile around')
    setTimeout(() => {
        flashEditProfile.style.display = 'none'
    }, 5000);
}
// HANDLE FLASH MESSAGES ON DASHBOARD ENDS HERE