let memberaction2 = document.querySelector('.memberaction2')
// let actiondots = document.querySelector('.actiondots')


// DISPLAY ACTION ON HOVER ON DOTS STARTS HERE
let actionbtns2 = document.querySelectorAll('.actionbtns2')
let actionbtns2b = document.querySelector('.actionbtns2')

actionbtns2.forEach(element => {
    element.addEventListener('click', () => {
        element.nextElementSibling.style.display = 'block'
    });
});


// HIDE DIV ON CLICK OUTSIDE
let memberaction = document.querySelectorAll('.memberaction2');
memberaction.forEach(element => {
    window.addEventListener('mouseup', function(event){
        if(event.target != element && event.target.parentNode != element){
            element.style.display = 'none';
        }
    }); 
})





















