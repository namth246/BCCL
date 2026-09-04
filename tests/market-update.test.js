const assert = require('assert');
const { parseReportWeek, mergeMarketUpdate } = require('../js/market-update.js');

const range = parseReportWeek('24/08/2026 - 28/08/2026');
assert.deepStrictEqual(range, { start: '2026-08-24', end: '2026-08-28' });

const current = {
  report: { week: '24/08/2026 - 28/08/2026', update_date: 'old', source: 'manual' },
  indices: [{ name: 'OLD' }],
  trading_value: '0',
  foreign_flow: [],
  market_conclusion: 'Giữ nguyên',
};
const update = {
  indices: [{ name: 'VNINDEX' }], trading_value: '1,500', foreign_flow: [{ date: '25/08', value: 277 }],
  meta: { updated_at: '04/09/2026', source: 'vnstock' },
};

const merged = mergeMarketUpdate(current, update);
assert.strictEqual(merged.market_conclusion, 'Giữ nguyên');
assert.strictEqual(merged.report.update_date, '04/09/2026');
assert.strictEqual(merged.report.source, 'vnstock');
assert.deepStrictEqual(merged.indices, update.indices);

console.log('PASS: market update helpers preserve manual data');
