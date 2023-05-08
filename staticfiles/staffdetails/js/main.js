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