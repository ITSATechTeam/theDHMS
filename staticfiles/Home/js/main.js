// ANIMATION NODE STARTS HERE

const scrollElements = document.querySelectorAll(".js-scroll");

const elementInView = (el, dividend = 1) => {
  const elementTop = el.getBoundingClientRect().top;

  return (
    elementTop <=
    (window.innerHeight || document.documentElement.clientHeight) / dividend
  );
};

const elementOutofView = (el) => {
  const elementTop = el.getBoundingClientRect().top;

  return (
    elementTop > (window.innerHeight || document.documentElement.clientHeight)
  );
};

const displayScrollElement = (element) => {
  element.classList.add("scrolled");
};

const hideScrollElement = (element) => {
  element.classList.remove("scrolled");
};

const handleScrollAnimation = () => {
  scrollElements.forEach((el) => {
    if (elementInView(el, 1.25)) {
      displayScrollElement(el);
    } else if (elementOutofView(el)) {
      hideScrollElement(el)
    }
  })
}

handleScrollAnimation()

window.addEventListener("scroll", () => { 
  handleScrollAnimation();
});

// ANIMATION NODE ENDS HERE


// HANDLE FLASH MESSAGES ON DASHBOARD STARTS HERE
let flashGeneral = document.querySelector('#flashmessage')
// let flashGeneral = document.querySelector('.alert strong')
if(flashGeneral){
    setTimeout(() => {
        flashGeneral.style.display = 'none'
    }, 5000);
}
// HANDLE FLASH MESSAGES ON DASHBOARD ENDS HERE