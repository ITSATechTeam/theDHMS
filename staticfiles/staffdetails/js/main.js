// PICK STAFF NAME ALPHABETS FOR DP STARTS HERE
let staffFirstName = document.querySelector('.staffFirstName').innerHTML
let staffLastName = document.querySelector('.staffLastName').innerHTML
let staffimgsection = document.querySelector('.staffimgsection h1')

let firstAlphabetFN;
let firstAlphabetLN;

for (let i = 0; i < staffFirstName.length; i++) {
    firstAlphabetFN = staffFirstName[0];
}


for (let i = 0; i < staffLastName.length; i++) {
    firstAlphabetLN = staffLastName[0];
}

staffimgsection.innerHTML = `${firstAlphabetFN}${firstAlphabetLN}`

// PICK STAFF NAME ALPHABETS FOR DP ENDS HERE
// registerDevice FORM POPUP STARTS HERE
let registerDevice = document.querySelector('.registerDevice')
let Shadow = document.querySelector('.shadow')
let closeaddnewdeviceopoup = document.querySelector('.closeaddnewdeviceopoup')
let staffdetailsaddtn = document.querySelector('.staffdetailsaddtn button')
staffdetailsaddtn.addEventListener('click', () => {
    registerDevice.style.display = 'Block'
    Shadow.style.display = 'block'
})

closeaddnewdeviceopoup.addEventListener('click', () => {
    registerDevice.style.display = 'none'
    Shadow.style.display = 'none'
})

// registerDevice FORM POPUP ENDS HERE