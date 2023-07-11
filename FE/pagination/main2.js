let data = [200000, undefined, undefined, undefined, 300000, 370000, 
    100000, undefined, undefined, 100000, undefined, 100000], result = data.map(v => v === undefined ? 0 : v);
console.log(result)