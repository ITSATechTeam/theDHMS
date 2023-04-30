// PROFILE IMAGE UPLOAD DETECTION STARTS HERE
// let profilepicture = document.querySelector('.profilepicture')
let profilepicture = document.querySelector('.uploadProfilePic')
let profileUpdateSection = document.querySelector('.profileUpdateSection')
let formsubmitbtn = document.querySelector('.formsubmitbtn')
let clickinfo = document.querySelector('.clickinfo')

// if(profilepicture > 0) {
  //   formsubmitbtn.style.display = 'block'
  // }
  
  profilepicture.addEventListener('click', () => {
  console.log("profilepicture")
  formsubmitbtn.style.display = 'block'
  clickinfo.style.display = 'none'
})

profileUpdateSection.addEventListener('mouseover', () => {
  clickinfo.style.display = 'block'
})

profileUpdateSection.addEventListener('mouseout', () => {
  clickinfo.style.display = 'none'
})