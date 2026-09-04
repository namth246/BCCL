const fs = require('fs');
const assert = require('assert');

const renderer = fs.readFileSync('js/renderer.js', 'utf8');

assert(
  renderer.includes("box(a,612,88,44,'#fff',c);text(`C>${n}`,a+44,625,80,10,C.navy,700,1.2,'center');text(`${Number(v).toFixed(2)}%`,a+44,646,80,17,c,700,1.2,'center')"),
  'Each MA label must render inside its own percentage box, above the value.'
);

console.log('PASS: MA labels use the balanced two-line box layout');
