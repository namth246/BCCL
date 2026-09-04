const fs = require('fs');
const assert = require('assert');

const core = fs.readFileSync('js/core.js', 'utf8');
const app = fs.readFileSync('js/app.js', 'utf8');
const renderer = fs.readFileSync('js/renderer.js', 'utf8');

assert(core.includes('market_metrics:{dji:'), 'Sample data must include market metrics');
assert(app.includes("['market_metrics.dji'"), 'DJI manual field is missing');
assert(app.includes("['market_metrics.oil'"), 'Oil manual field is missing');
assert(app.includes("['market_metrics.bitcoin'"), 'Bitcoin manual field is missing');
assert(core.includes("x=x[a[i]]??(x[a[i]]={})"), 'Nested manual fields must work with existing saved JSON');
assert(renderer.includes("['DowJone',metrics.dji]"), 'Renderer must draw the DJI table cell');
assert(renderer.includes('metrics.oil'), 'Renderer must draw the oil table cell');
assert(renderer.includes("['BITCOIN',metrics.bitcoin]"), 'Renderer must draw the Bitcoin table cell');
assert(renderer.includes("newsText(d.news.global,1132,910,220)"), 'News must retain its dedicated content area below the table');

console.log('PASS: market metrics table and manual fields are configured');
