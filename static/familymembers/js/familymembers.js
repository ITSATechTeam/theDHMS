
let familymemberintrobtn = document.querySelector('.familymemberintrobtn button')
let addfampopup = document.querySelector('.addfampopup')
let shadow = document.querySelector('.shadow')
let addfampopupheadclosebtn = document.querySelector('.addfampopupheadclosebtn')

if (familymemberintrobtn){
    familymemberintrobtn.addEventListener('click', () => {
        addfampopup.style.display = 'block'
        shadow.style.display = 'block'
    })
}


if(addfampopupheadclosebtn){
    addfampopupheadclosebtn.addEventListener('click', () => {
        addfampopup.style.display = 'none'
        shadow.style.display = 'none'
    })

}

// HANDLE FLASH MESSAGES ON FAMILY MEMBER AREA STARTS HERE
let flashfammember = document.querySelector('#flash')
if (flashfammember){
    setInterval(() => {
        flashfammember.style.display = 'none'
    }, 5000);
}
// HANDLE FLASH MESSAGES ON FAMILY MEMBER AREA ENDS HERE

// NO FAMILY MEMBER YET SETUP STARTS HERE
let familymemberCount = document.querySelector('.familymemberCount p').innerHTML
let mainfamilymemberslistsection = document.querySelector('.mainfamilymemberslistsection')
let emptystate = document.querySelector('.emptystate')


if (familymemberCount === '0'){
    mainfamilymemberslistsection.style.display = 'none'
    emptystate.style.display = 'block'
}else{
    mainfamilymemberslistsection.style.display = 'block'
    emptystate.style.display = 'none'
}

// DISPLAY ACTION ON HOVER ON DOTS STARTS HERE
let actionbtns = document.querySelectorAll('.actionbtns')

actionbtns.forEach(element => {
    element.addEventListener('click', () => {
        // console.log(element.nextElementSibling )
        element.nextElementSibling.style.display = 'block'
    });
});

// HIDE DIV ON CLICK OUTSIDE
let memberaction = document.querySelectorAll('.memberaction');
memberaction.forEach(element => {
    window.addEventListener('mouseup', function(event){
        if(event.target != element && event.target.parentNode != element){
            element.style.display = 'none';
        }
    }); 
})



let addsubadmin  = document.querySelector('.addsubadmin')
let addsubadminclosebtn  = document.querySelectorAll('.addsubadminclosebtn')
let addsubadminbtnscancel  = document.querySelectorAll('.addsubadminbtnscancel')

addsubadminclosebtn.forEach(element => {
    element.addEventListener('click', () => {
        element.parentElement.style.display = 'none'
        shadow.style.display = 'none'
    })
});


addsubadminbtnscancel.forEach(element => {
    element.addEventListener('click', () => {
        element.parentElement.parentElement.parentElement.style.display = 'none'
        shadow.style.display = 'none'
    })
});


let memberactioninner = document.querySelectorAll('.memberactioninner')
memberactioninner.forEach(element => {
    element.addEventListener('click', () => {
        shadow.style.display = 'block'
        element.parentNode.nextElementSibling.style.display = 'block'
    });
});



let newsubadminclosebtn  = document.querySelector('.newsubadminclosebtn')
let newsubadmin  = document.querySelector('.newsubadmin')


let alertprompt = document.querySelector('.alert strong').innerHTML

if (alertprompt === "You added a subadmin on your account"){
    newsubadmin.style.display = 'block'
    shadow.style.display = 'block'

}

newsubadminclosebtn.addEventListener('click', () => {
    if (newsubadmin){
        newsubadmin.style.display = 'none'
        shadow.style.display = 'none'
    }
})














