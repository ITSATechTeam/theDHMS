

// PREVIEW UPLOADED IMAGE FUNCTIONALITY STARTS HERE
let previewimage = document.querySelector('#previewimage')
let uploadedimage = document.querySelector('#images')

uploadedimage.onchange = () => {
    const [file] = uploadedimage.files
    if (file) {
        previewimage.style.display = 'block'
        previewimage.src = URL.createObjectURL(file)
    }
}
// PREVIEW UPLOADED IMAGE FUNCTIONALITY ENDS HERE

let registerDeviceinv = document.querySelector('.registerDeviceinv')
let shadow = document.querySelector('.shadow')
let closeaddnewdeviceopoup = document.querySelector('.closeaddnewdeviceopoup')
let addnewdevicebtn = document.querySelector('.addnewdevicebtn button')
let emptystatebtn = document.querySelector('.emptystate button')


emptystatebtn.addEventListener('click', () => {
    shadow.style.display = 'block'
    registerDeviceinv.style.display = 'block'
})

addnewdevicebtn.addEventListener('click', () => {
    shadow.style.display = 'block'
    registerDeviceinv.style.display = 'block'
})

closeaddnewdeviceopoup.addEventListener('click', () => {
    shadow.style.display = 'none'
    registerDeviceinv.style.display = 'none'
})

let deviceregsuccess = document.querySelector('.deviceregsuccess')
let closedeviceregsuccess = document.querySelector('.closedeviceregsuccess')
let alertText = document.querySelector('.alert strong').innerHTML

if (alertText === "Device registered successfully."){
    deviceregsuccess.style.display = "block"
    shadow.style.display = "block"
}

closedeviceregsuccess.addEventListener('click', () => {
    deviceregsuccess.style.display = "none"
    shadow.style.display = "none"
})



// imgInp.onchange = evt => {
//     const [file] = imgInp.files
//     if (file) {
//       blah.src = URL.createObjectURL(file)
//     }
//   }
//   <form runat="server">
//     <input accept="image/*" type='file' id="imgInp" />
//     <img id="blah" src="#" alt="your image" />
//   </form>




