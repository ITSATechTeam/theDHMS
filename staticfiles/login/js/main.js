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

