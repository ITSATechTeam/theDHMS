const registerstaffbox = document.querySelector('.regsiteruser');
const addstaffbtn = document.querySelector('.addstaffbtn button');
const closereguser = document.querySelector('.closereguser');
const shadow1 = document.querySelector('.shadow1');

addstaffbtn.addEventListener('click', () => {
	registerstaffbox.style.display = 'block';
	shadow1.style.display = 'block';
})

closereguser.addEventListener('click', () => {
	registerstaffbox.style.display = 'none';
	shadow1.style.display = 'none';
})