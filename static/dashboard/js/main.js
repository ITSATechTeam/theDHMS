const filtercategory = document.querySelector('.filtercategory')
const filtercalendar = document.querySelector('.filtercalendar')
const shadow = document.querySelector('.shadow')
const filterbox1 = document.querySelector('.filterbox1')
const filterbox2 = document.querySelector('.filterbox2')
const closefilter = document.querySelector('.closefilter')
const closefilter2 = document.querySelector('.closefilter2')
const body = document.querySelector('.body')
// FILTER BY CATEGORY SECTION STARTS HERE
const filterbox1A = document.querySelector('.filterbox1A')
const filtercategory2 = document.querySelector('.filtercategory2')
const closefilterA = document.querySelector('.closefilterA')

filtercategory2.addEventListener('click', () => {
    console.log('close filter')
    shadow.style.display = 'block';
    filterbox1A.style.display = 'block'
})


closefilterA.addEventListener('click', () => {
    shadow.style.display = 'none';
    filterbox1A.style.display = 'none'
})

// FILTER BY CATEGORY SECTION ENDS HERE



filtercategory.addEventListener('click', () =>{
    shadow.style.display = 'block';
    filterbox1.style.display = 'block';
    // shadow.style.height === body.style.height
})

closefilter.addEventListener('click', () =>{
    shadow.style.display = 'none';
    filterbox1.style.display = 'none';

})
closefilter2.addEventListener('click', () =>{
    shadow.style.display = 'none';
    filterbox2.style.display = 'none';

})


filtercalendar.addEventListener('click', () =>{
    shadow.style.display = 'block';
    filterbox2.style.display = 'block';
})



// ADD DEVICE POPUP STARTS HERE
let addnewdevicebtn = document.querySelector('.addnewdevicebtn')
let registerDevice = document.querySelector('.registerDevice')
let closeaddnewdeviceopoup = document.querySelector('.closeaddnewdeviceopoup')

addnewdevicebtn.addEventListener('click', () => {
    registerDevice.style.display = 'block'
    shadow.style.display = 'block'
})
closeaddnewdeviceopoup.addEventListener('click', () => {
    registerDevice.style.display = 'none'
    shadow.style.display = 'none'
})
// ADD DEVICE POPUP ENDS HERE


// UPLOAD CSV FILE STARTS POPUP HERE
let uploaddevicepopupintroclose = document.querySelector('.uploaddevicepopupintroclose')
let uploaddevicepopup = document.querySelector('.uploaddevicepopup')
let showdeviceuploadpopup = document.querySelector('.showdeviceuploadpopup')



showdeviceuploadpopup.addEventListener('click', () => {
    // console.log('showdeviceuploadpopup clicked')
    uploaddevicepopup.style.display = 'block'
    shadow.style.display = 'block';
})


uploaddevicepopupintroclose.addEventListener('click', () => {
    uploaddevicepopup.style.display = 'none'
    shadow.style.display = 'none';
})



// DATE AND TIME SEARVH EDITS STARTS HERE
const thismonth = document.querySelector('.thismonth')
const lastMonth = document.querySelector('.lastMonth')
const thisweek = document.querySelector('.thisweek')
const lastweek = document.querySelector('.lastweek')
const month = ["January","February","March","April","May","June","July","August","September","October","November","December"];
const newDate = new Date();
let currentMonth = month [newDate.getMonth()];
let previousMonth = month [newDate.getMonth() - 1];
thismonth.value = currentMonth
lastMonth.value = previousMonth


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
thisweek.value = `${weekNumber}`;
lastweek.value = `${weekNumber- 1}` ;

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

closeCompleteProfilePrompt.addEventListener('click', () => {
    completeDetailsPopup.style.display = 'none'
    shadowForPreReg.style.display = 'none'
})


// completeDetailsPopup SETUP ENDS HERE