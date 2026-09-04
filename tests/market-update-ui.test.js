const fs = require('fs');
const assert = require('assert');

const index = fs.readFileSync('index.html', 'utf8');
const ui = fs.readFileSync('js/market-update-ui.js', 'utf8');

assert(index.includes('js/market-update.js'), 'Market update helper must load before app.js');
assert(index.includes('id="update-market-button"'), 'Market update button is missing');
assert(index.includes('js/market-update-ui.js'), 'Market update UI controller must load');
assert(ui.includes('updateMarketData'), 'UI controller must handle the update action');
assert(ui.includes('MarketUpdate.parseReportWeek'), 'UI controller must validate the report week');
assert(ui.includes('MARKET_UPDATE_ENDPOINT'), 'UI controller must call the local market endpoint');

const button = { disabled: false, textContent: 'Cập nhật dữ liệu', addEventListener: (_, handler) => { button.handler = handler; } };
const status = { textContent: '' };
const week = { value: '25/08/2026 - 28/08/2026', type: 'text', dataset: { path: 'report.week' } };
const conclusion = { value: 'Giữ nhận định thủ công.', type: 'text', dataset: { path: 'market_conclusion' } };
const stored = {};
let requestedUrl = '';

global.document = {
  querySelector: selector => ({ '#update-market-button': button, '#status': status, '#f-report-week': week }[selector]),
  querySelectorAll: () => [week, conclusion],
};
global.location = { protocol: 'http:', reload: () => { global.reloaded = true; } };
global.localStorage = { setItem: (key, value) => { stored[key] = JSON.parse(value); } };
global.window = { setTimeout: callback => callback() };
global.MARKET_UPDATE_ENDPOINT = '/api/market-week';
global.STORAGE_KEY = 'cnf-weekly-report-v1';
global.fetch = async url => {
  requestedUrl = url;
  return {
    ok: true,
    json: async () => ({
      meta: { updated_at: '28/08/2026', source: 'vnstock Silver' },
      indices: [{ name: 'VNINDEX', close: '1,800', change: '+10', percent: '+0.5%' }],
      trading_value: '20,000',
      foreign_flow: [{ date: '28/08', value: 100 }],
    }),
  };
};

require('../js/market-update.js');
require('../js/market-update-ui.js');

(async () => {
  await button.handler();
  assert(requestedUrl.includes('start=2026-08-25'), 'Click must send the parsed start date');
  assert(requestedUrl.includes('end=2026-08-28'), 'Click must send the parsed end date');
  assert.equal(stored['cnf-weekly-report-v1'].trading_value, '20,000');
  assert.equal(stored['cnf-weekly-report-v1'].market_conclusion, 'Giữ nhận định thủ công.');
  assert.equal(global.reloaded, true, 'Click must reload the report with the updated data');
  console.log('PASS: market update UI is wired and responds to a click');
})().catch(error => { console.error(error); process.exitCode = 1; });
