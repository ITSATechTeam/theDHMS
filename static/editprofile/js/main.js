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

