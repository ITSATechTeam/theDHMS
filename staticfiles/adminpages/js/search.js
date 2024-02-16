// const filtercategory = document.querySelector('.filtercategory')
const filtercalendar = document.querySelector('.filtercalendar')
const shadow = document.querySelector('.shadow')
const filterbox1 = document.querySelector('.filterbox1')
const filterbox2 = document.querySelector('.filterbox2')
const closefilter = document.querySelector('.closefilter')
const closefilter2 = document.querySelector('.closefilter2')
const body = document.querySelector('.body')




// filtercategory.addEventListener('click', () =>{
//     shadow.style.display = 'block';
//     filterbox1.style.display = 'block';
//     // shadow.style.height === body.style.height
// })

// closefilter.addEventListener('click', () =>{
//     shadow.style.display = 'none';
//     filterbox1.style.display = 'none';

// })
// closefilter2.addEventListener('click', () =>{
//     shadow.style.display = 'none';
//     filterbox2.style.display = 'none';

// })


// filtercalendar.addEventListener('click', () =>{
//     shadow.style.display = 'block';
//     filterbox2.style.display = 'block';
// })



// // ADD DEVICE POPUP STARTS HERE
// let addnewdevicebtn = document.querySelector('.addnewdevicebtn')
// let registerDevice = document.querySelector('.registerDevice')
// let closeaddnewdeviceopoup = document.querySelector('.closeaddnewdeviceopoup')

// addnewdevicebtn.addEventListener('click', () => {
//     registerDevice.style.display = 'block'
//     shadow.style.display = 'block'
// })
// closeaddnewdeviceopoup.addEventListener('click', () => {
//     registerDevice.style.display = 'none'
//     shadow.style.display = 'none'
// })
// // ADD DEVICE POPUP ENDS HERE


// // UPLOAD CSV FILE STARTS POPUP HERE
// let uploaddevicepopupintroclose = document.querySelector('.uploaddevicepopupintroclose')
// let uploaddevicepopup = document.querySelector('.uploaddevicepopup')
// let showdeviceuploadpopup = document.querySelector('.showdeviceuploadpopup')



// showdeviceuploadpopup.addEventListener('click', () => {
//     console.log('showdeviceuploadpopup clicked')
//     uploaddevicepopup.style.display = 'block'
//     shadow.style.display = 'block';
// })


// uploaddevicepopupintroclose.addEventListener('click', () => {
//     uploaddevicepopup.style.display = 'none'
//     shadow.style.display = 'none';
// })



// DATE AND TIME SEARVH EDITS STARTS HERE
const thismonth = document.querySelector('.thismonth')
const lastMonth = document.querySelector('.lastMonth')
const thisweek = document.querySelector('.thisweek')
const lastweek = document.querySelector('.lastweek')
const month = ["January","February","March","April","May","June","July","August","September","October","November","December"];
const newDate = new Date();
let currentMonth = month[newDate.getMonth()];
let previousMonth = month[newDate.getMonth() - 1];
// thismonth.value = currentMonth
// lastMonth.value = previousMonth


// const d = new Date();
// let name = month[d.getMonth()];

// calculte current week 

currentDate = new Date();
startDate = new Date(currentDate.getFullYear(), 0, 1);
var days = Math.floor((currentDate - startDate) /
    (24 * 60 * 60 * 1000));

var weekNumber = Math.ceil(days / 7);
    
// Display the calculated result      
console.log("Week number of " + currentDate +
    " is :   " + weekNumber);

// send in current and previous week number
// thisweek.value = `week${weekNumber}`;
// lastweek.value = `week${weekNumber- 1}` ;

// current yeah
let date =  new Date().getFullYear();
console.log(date);


// send main savetimedata pack to db
const savetimedata = document.querySelector('.sendsavetimedata');
// savetimedata.value = `currentWeek is week${weekNumber} and this month is month${currentMonth} and this year is year${date}`
console.log(weekNumber)



// console.log(`currentWeek is week${weekNumber} and this month is month${currentMonth} and this year is year${date}`);

