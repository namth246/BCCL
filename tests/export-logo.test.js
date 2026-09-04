const fs = require('fs');
const assert = require('assert');

const index = fs.readFileSync('index.html', 'utf8');
const app = fs.readFileSync('js/app.js', 'utf8');

assert(index.includes('js/logo-data.js'), 'Logo must be embedded before app.js loads');
assert(app.includes("loadAsset('logo',LOGO_DATA_URI)"), 'Logo must load from the embedded data URI');
assert(app.includes('function exportPng()'), 'PNG export must use a guarded export function');
assert(app.includes('catch(err)'), 'PNG export must handle exceptions');
assert(app.includes('exportBtn.onclick=exportPng'), 'Export button must use the guarded export function');

console.log('PASS: embedded logo and guarded PNG export are configured');
