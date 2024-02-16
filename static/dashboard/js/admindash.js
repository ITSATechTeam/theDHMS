// CUSTOM GREETING SETUP STARTS HERE
var myDate = new Date();
var hrs = myDate.getHours();

var greet;

if (hrs < 12)
  greet = 'Good Morning';
else if (hrs >= 12 && hrs <= 16)
greet = 'Good Afternoon';
else if (hrs >= 16 && hrs <= 20)
greet = 'Good Evening';
else if (hrs >= 21 && hrs <= 24)
greet = 'You should be in bed now';

document.querySelector('.greetuseradmin').innerHTML = greet;

// CUSTOM GREETING SETUP ENDS HERE


//   FILL SHAPE WITH FIRST LETTER FUNCTIONALITY STARTS HERE
let companyname = document.querySelectorAll('.companyname')
companyname.forEach((e) => {
    e.parentElement.previousElementSibling.innerHTML = Array.from(e.innerHTML)[0]
})



const filtercategory = document.querySelector('.filtercategory')
const filtercalendar = document.querySelector('.filtercalendar')
const shadow = document.querySelector('.shadow1')
const filterbox1 = document.querySelector('.filterbox1')
const filterbox2 = document.querySelector('.filterbox2')
const closefilter = document.querySelector('.closefilter')
const closefilter2 = document.querySelector('.closefilter2')
const body = document.querySelector('.body')
// FILTER BY CATEGORY SECTION STARTS HERE
const filterbox1A = document.querySelector('.filterbox1A')
const filtercategory2 = document.querySelector('.filtercategory2')
const closefilterA = document.querySelector('.closefilterA')

// HANDLE FLASH MESSAGES ON DASHBOARD STARTS HERE
let flashGeneraldash = document.querySelector('#flashmessage')
// let flashGeneral = document.querySelector('.alert strong')
if(flashGeneraldash){
    setTimeout(() => {
        flashGeneraldash.style.display = 'none'
    }, 5000);
}
// HANDLE FLASH MESSAGES ON DASHBOARD ENDS HERE

if(filtercategory2){
    filtercategory2.addEventListener('click', () => {
        // console.log('close filter')
        shadow.style.display = 'block';
        filterbox1A.style.display = 'block'
    })
}

if (closefilterA){
closefilterA.addEventListener('click', () => {
    shadow.style.display = 'none';
    filterbox1A.style.display = 'none'
})
}

// FILTER BY CATEGORY SECTION ENDS HERE


if (filtercategory){
    filtercategory.addEventListener('click', () =>{
        shadow.style.display = 'block';
        filterbox1.style.display = 'block';
        // shadow.style.height === body.style.height
    })
}

if(closefilter){
    closefilter.addEventListener('click', () =>{
        shadow.style.display = 'none';
        filterbox1.style.display = 'none';
    })
}


if(closefilter2){
    closefilter2.addEventListener('click', () =>{
        shadow.style.display = 'none';
        filterbox2.style.display = 'none';
    
    })
}

if (filtercalendar){
filtercalendar.addEventListener('click', () =>{
    shadow.style.display = 'block';
    filterbox2.style.display = 'block';
    })
}



// ADD DEVICE POPUP STARTS HERE
let addnewdevicebtn = document.querySelector('.addnewdevicebtn')
let registerDevice = document.querySelector('.registerDevice')
let closeaddnewdeviceopoup = document.querySelector('.closeaddnewdeviceopoup')

if (addnewdevicebtn){
    addnewdevicebtn.addEventListener('click', () => {
        registerDevice.style.display = 'block'
        shadow.style.display = 'block'
    })
}
closeaddnewdeviceopoup.addEventListener('click', () => {
    registerDevice.style.display = 'none'
    shadow.style.display = 'none'
})
// ADD DEVICE POPUP ENDS HERE


// UPLOAD CSV FILE STARTS POPUP HERE
let uploaddevicepopupintroclose = document.querySelector('.uploaddevicepopupintroclose')
let uploaddevicepopup = document.querySelector('.uploaddevicepopup')
let showdeviceuploadpopup = document.querySelector('.showdeviceuploadpopup')


if(showdeviceuploadpopup){
    showdeviceuploadpopup.addEventListener('click', () => {
        uploaddevicepopup.style.display = 'block'
        shadow.style.display = 'block';
    })
}


if(uploaddevicepopupintroclose){
uploaddevicepopupintroclose.addEventListener('click', () => {
    uploaddevicepopup.style.display = 'none'
    shadow.style.display = 'none';
})
}



// DATE AND TIME SEARVH EDITS STARTS HERE
const thismonth = document.querySelector('.thismonth')
const lastMonth = document.querySelector('.lastMonth')
const thisweek = document.querySelector('.thisweek')
const lastweek = document.querySelector('.lastweek')
const month = ["January","February","March","April","May","June","July","August","September","October","November","December"];
const newDate = new Date();
let currentMonth = month [newDate.getMonth()];
let previousMonth = month [newDate.getMonth() - 1];
if(thismonth){
    thismonth.value = currentMonth
}

if(lastMonth){
    lastMonth.value = previousMonth
}


// const d = new Date();
// let name = month[d.getMonth()];

// calculte current week 

currentDate = new Date();
startDate = new Date(currentDate.getFullYear(), 0, 1);
var days = Math.floor((currentDate - startDate) /
    (24 * 60 * 60 * 1000));

var weekNumber = Math.ceil(days / 7);

// Display the calculated result      
// console.log("Week number of " + currentDate +
//     " is :   " + weekNumber);

// send in current and previous week number
if(thisweek){
    thisweek.value = `${weekNumber}`;
}
if(lastweek){
    lastweek.value = `${weekNumber- 1}` ;
}

// current yeah
let date =  new Date().getFullYear();
// console.log(date);


// send main savetimedata pack to db
const savetimedata = document.querySelector('.sendsavetimedata');
savetimedata.value = 'currentWeek is week '+ weekNumber +' and this month is ' + currentMonth +' and this year is year '+ date 
// console.log(weekNumber)

// console.log('currentWeek is   ' + weekNumber +' and this month is  '+ currentMonth +' and this year is ' +date );

// enterStaffUser DEFAULT DATA ALLOCATION FUNCTIONALITY STARTS HERE
// let enterStaffUser = Array.from(document.querySelectorAll('.enterStaffUser'));
// let enterStaffUserArr = []
// console.log(typeof(enterStaffUser))
// enterStaffUser.forEach(e => {
//     enterStaffUserArr.push(e)
//     if(e === ' '){
//         enterStaffUser = 'None'
//     }    
// });

// enterStaffUserArr.forEach(element => {
//     console.log(element.innerHTML)
//     if(element.innerHTML === "" ){
//         element.innerHTML = 'None'
//     }    
// });

// console.log(enterStaffUserArr)

// enterStaffUser DEFAULT DATA ALLOCATION FUNCTIONALITY ENDS HERE
// completeDetailsPopup SETUP STARTS HERE
let closeCompleteProfilePrompt = document.querySelector('.closeCompleteProfilePrompt')
let completeDetailsPopup = document.querySelector('.completeDetailsPopup')
let shadowForPreReg = document.querySelector('.shadowForPreReg')

if (closeCompleteProfilePrompt){
    closeCompleteProfilePrompt.addEventListener('click', () => {
        completeDetailsPopup.style.display = 'none'
        shadowForPreReg.style.display = 'none'
    })
}


// completeDetailsPopup SETUP ENDS HERE

let dashboardStaffDP = document.querySelectorAll('.dashboardStaffDP')
let staffIdSection = document.querySelectorAll('.staffIdSection')
let allDivAr = []
staffIdSection.forEach((e)=>{
    if (e.innerHTML.slice(-1) < 4){
        e.parentElement.previousElementSibling.style.backgroundColor = "#FFE7664D"
    }else if(e.innerHTML.slice(-1) > 8){
        e.parentElement.previousElementSibling.style.backgroundColor = "#7DF2AF4D"
    }
  })

//   FILL SHAPE WITH FIRST LETTER FUNCTIONALITY STARTS HERE
let staffnamesection = document.querySelectorAll('.staffnamesection')
// console.log(staffnamesection)
staffnamesection.forEach((e) => {
    e.parentElement.previousElementSibling.innerHTML = Array.from(e.innerHTML)[0]
})


// MAINTENANCE SECTION ON THE DASHBOARD
let maintenanceStatus = document.querySelectorAll('.maintenanceStatusMain')
maintenanceStatus.forEach((e) => {
    if (e.innerHTML === 'Pending'){
        e.style.color = "#27AE60"
        e.previousSibling.style.backgroundColor = "#B2B3B5";
    }else if(e.innerHTML === 'Ongoing'){
        e.style.color = "#F2994A"
        e.previousSibling.style.backgroundColor = "#F2994A";
    }else if(e.innerHTML === 'Completed'){
        e.style.color = "#27AE60"
        e.previousSibling.style.backgroundColor = "#27AE60";
    }else if(e.innerHTML === 'Cancelled'){
        e.style.color = "#EB5757";
        e.previousSibling.style.backgroundColor = "#EB5757";
    }
})


let maintenanceType = document.querySelectorAll('.maintenanceType')
maintenanceType.forEach((e) => {
    // console.log(e)
    shortenString = e.innerHTML.substring(0, 15).concat('...')
    e.innerHTML = shortenString
})










