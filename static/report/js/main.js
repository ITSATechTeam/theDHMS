let AllMonthArray = [];
// JANUARY CALCULATION STARTS HERE
let janelement =[];
let janelementMain2;
let janSum;
let janDevices = document.querySelectorAll('.JanDevices')
janDevices.forEach(element => {
  janelementMain2 = element.innerText;
    janelement.push(janelementMain2)
    janSum = janelement.map( function(elt){ // assure the value can be converted into an integer
      return /^\d+$/.test(elt) ? parseInt(elt) : 0; 
    })
    .reduce( function(a,b){ // sum all resulting numbers
      return a+b
    });
    
  });
  console.log(janSum)
  AllMonthArray.push(janSum);

  let AllMonthArrayData = document.querySelector('.AllMonthArray').value
  AllMonthArrayData = AllMonthArray
// JANUARY CALCULATION ENDS HERE

// FEBRUARY CALCULATION STARTS HERE
let febelement =[];
let febelementMain2;
let febSum;
let febDevices = document.querySelectorAll('.FebDevices')
febDevices.forEach(element => {
  febelementMain2 = element.innerText;
    febelement.push(febelementMain2)
    febSum = febelement.map( function(elt){ // assure the value can be converted into an integer
      return /^\d+$/.test(elt) ? parseInt(elt) : 0; 
    })
    .reduce( function(a,b){ // sum all resulting numbers
      return a+b
    });
    
  });
  console.log(febSum)
  AllMonthArray.push(febSum);
// FEBRUARY CALCULATION ENDS HERE

// MARCH CALCULATION STARTS HERE
let marelement =[];
let marelementMain2;
let marSum;
let marDevices = document.querySelectorAll('.MarDevices')
marDevices.forEach(element => {
  marelementMain2 = element.innerText;
    marelement.push(marelementMain2)
    marSum = marelement.map( function(elt){ // assure the value can be converted into an integer
      return /^\d+$/.test(elt) ? parseInt(elt) : 0; 
    })
    .reduce( function(a,b){ // sum all resulting numbers
      return a+b
    });
    
  });
  console.log(marSum)
  AllMonthArray.push(marSum);
// MARCH CALCULATION ENDS HERE

// APRIL CALCULATION STARTS HERE
let aprelement =[];
let aprelementMain2;
let aprSum;
let aprDevices = document.querySelectorAll('.AprDevices')
aprDevices.forEach(element => {
  aprelementMain2 = element.innerText;
    aprelement.push(aprelementMain2)
    aprSum = aprelement.map( function(elt){ // assure the value can be converted into an integer
      return /^\d+$/.test(elt) ? parseInt(elt) : 0; 
    })
    .reduce( function(a,b){ // sum all resulting numbers
      return a+b
    });
    
  });
  console.log(aprSum)
  AllMonthArray.push(aprSum);
// APRIL CALCULATION ENDS HERE

// MAY CALCULATION STARTS HERE
let mayelement =[];
let mayelementMain2;
let maySum;
let mayDevices = document.querySelectorAll('.MayDevices')
mayDevices.forEach(element => {
  mayelementMain2 = element.innerText;
    mayelement.push(mayelementMain2)
    maySum = mayelement.map( function(elt){ // assure the value can be converted into an integer
      return /^\d+$/.test(elt) ? parseInt(elt) : 0; 
    })
    .reduce( function(a,b){ // sum all resulting numbers
      return a+b
    });
    
  });
  console.log(maySum)
  AllMonthArray.push(maySum);
// MAY CALCULATION ENDS HERE


// JUNE CALCULATIONS STARTS HERE
let juneelement =[];
let juneelementMain2;
let JuneSum;
let JuneDevices = document.querySelectorAll('.JuneDevices')
JuneDevices.forEach(element => {
  juneelementMain2 = element.innerText;
  juneelement.push(juneelementMain2)
    JuneSum = juneelement.map( function(elt){ // assure the value can be converted into an integer
      return /^\d+$/.test(elt) ? parseInt(elt) : 0; 
    })
    .reduce( function(a,b){ // sum all resulting numbers
      return a+b
    });
    
  });
  console.log(JuneSum)
  AllMonthArray.push(JuneSum);
// JUNE CALCULATIONS ENDS HERE

// JULY CALCULATIONS STARTS HERE
let julyelement =[];
let julyelementMain2;
let julySum;
let julyDevices = document.querySelectorAll('.JulyDevices')
julyDevices.forEach(element => {
  julyelementMain2 = element.innerText;
    julyelement.push(julyelementMain2)
    julySum = julyelement.map( function(elt){ // assure the value can be converted into an integer
      return /^\d+$/.test(elt) ? parseInt(elt) : 0; 
    })
    .reduce( function(a,b){ // sum all resulting numbers
      return a+b
    });
    
  });
  console.log(julySum)
  AllMonthArray.push(julySum);
// JULY CALCULATIONS ENDS HERE

// AUGUST CALCULATIONS STARTS HERE
let augelement =[];
let augelementMain2;
let augSum;
let augDevices = document.querySelectorAll('.AugDevices')
augDevices.forEach(element => {
  augelementMain2 = element.innerText;
    augelement.push(augelementMain2)
    augSum = augelement.map( function(elt){ // assure the value can be converted into an integer
      return /^\d+$/.test(elt) ? parseInt(elt) : 0; 
    })
    .reduce( function(a,b){ // sum all resulting numbers
      return a+b
    });
    
  });
  console.log(augSum)
  AllMonthArray.push(augSum);
// AUGUST CALCULATIONS ENDS HERE

// SEPTEMBER CALCULATIONS STARTS HERE
let septelement =[];
let septelementMain2;
let septSum;
let septDevices = document.querySelectorAll('.septDevices')
septDevices.forEach(element => {
  septelementMain2 = element.innerText;
    septelement.push(septelementMain2)
    septSum = septelement.map( function(elt){ // assure the value can be converted into an integer
      return /^\d+$/.test(elt) ? parseInt(elt) : 0; 
    })
    .reduce( function(a,b){ // sum all resulting numbers
      return a+b
    });
    
  });
  console.log(septSum)
  AllMonthArray.push(septSum);
// SEPTEMBER CALCULATIONS ENDS HERE

// OCTOBER CALCULATIONS STARTS HERE
let octtelement =[];
let octtelementMain2;
let octtSum;
let octtDevices = document.querySelectorAll('.OctDevices')
octtDevices.forEach(element => {
  octtelementMain2 = element.innerText;
    octtelement.push(octtelementMain2)
    octtSum = octtelement.map( function(elt){ // assure the value can be converted into an integer
      return /^\d+$/.test(elt) ? parseInt(elt) : 0; 
    })
    .reduce( function(a,b){ // sum all resulting numbers
      return a+b
    });
    
  });
  console.log(octtSum)
  AllMonthArray.push(octtSum);
// OCTOBER CALCULATIONS ENDS HERE

// NOVEMBER CALCULATIONS STARTS HERE
let novtelement =[];
let novtelementMain2;
let novtSum;
let novtDevices = document.querySelectorAll('.NovDevices')
novtDevices.forEach(element => {
  novtelementMain2 = element.innerText;
    novtelement.push(novtelementMain2)
    novtSum = novtelement.map( function(elt){ // assure the value can be converted into an integer
      return /^\d+$/.test(elt) ? parseInt(elt) : 0; 
    })
    .reduce( function(a,b){ // sum all resulting numbers
      return a+b
    });
    
  });
  console.log(novtSum)
  AllMonthArray.push(novtSum);
// NOVEMBER CALCULATIONS ENDS HERE

// DECEMBER CALCULATIONS STARTS HERE
let dectelement =[];
let dectelementMain2;
let dectSum;
let dectDevices = document.querySelectorAll('.DecDevices')
dectDevices.forEach(element => {
  dectelementMain2 = element.innerText;
    dectelement.push(dectelementMain2)
    dectSum = dectelement.map( function(elt){ // assure the value can be converted into an integer
      return /^\d+$/.test(elt) ? parseInt(elt) : 0; 
    })
    .reduce( function(a,b){ // sum all resulting numbers
      return a+b
    });
    
  });
  console.log(dectSum)
  AllMonthArray.push(dectSum);

console.log(AllMonthArray)
let AllMonthArrayMain = AllMonthArray.filter(
    element => typeof element === 'number'
)
console.log(AllMonthArrayMain)


// SECOND GRAPH SET UP STARTS HERE
let Amounts = ['100,000', '200,000', '300,000', '400,000', '500,000']
let AllMonthArray2 = ['100,000', '200,000', '300,000', '400,000', '500,000']
let pie = document.querySelector('#pie-chart2')


var config = {
  type: 'doughnut',
  data: {
    datasets: [{
    data: AllMonthArray2, 
    backgroundColor: [
      'rgba(64, 100, 255, 0.39)',
      '#2A66B0',
      'rgba(64, 100, 255, 0.39)',
      '#2A66B0',
      'rgba(64, 100, 255, 0.39)',
      '#2A66B0',
      'rgba(64, 100, 255, 0.39)',
      '#2A66B0',
      'rgba(64, 100, 255, 0.39)',
      '#2A66B0',
      'rgba(64, 100, 255, 0.39)',
      '#2A66B0' 
    ],
    label: 'Amount Spent On Hardware Purchase'
    }],
    labels: Amounts
  },
  options: {
    responsive: true,
    legend: {
    display: false
  }
    
  }
  };

  window.onload = function() {
  var ctx = pie.getContext('2d');
  // var ctx = document.getElementById('pie').getContext('2d');
  window.myPie = new Chart(ctx, config);
  };			

// SECOND GRAPH SET UP ENDS HERE
