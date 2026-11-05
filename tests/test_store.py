# Tests for window.ADAStore (P1 Export / Import progress & merge rules)
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE_JS = os.path.join(ROOT, 'src', 'js', 'store.js')

def main():
    if not os.path.exists(STORE_JS):
        print('FAIL: src/js/store.js does not exist')
        sys.exit(1)

    node_test = r"""
const fs = require('fs');
const code = fs.readFileSync(process.argv[1], 'utf8');

// Mock browser environment
const store = {};
global.localStorage = {
  getItem: (k) => Object.prototype.hasOwnProperty.call(store, k) ? store[k] : null,
  setItem: (k, v) => { store[k] = String(v); },
  removeItem: (k) => { delete store[k]; },
  clear: () => { for (const k of Object.keys(store)) delete store[k]; }
};
global.window = global;
global.document = {
  addEventListener: () => {},
  getElementById: () => null,
  createElement: () => ({ style: {}, appendChild: () => {}, addEventListener: () => {} })
};

eval(code);

function assert(cond, msg) {
  if (!cond) {
    console.error('FAIL:', msg);
    process.exit(1);
  }
}

assert(typeof window.ADAStore === 'object', 'window.ADAStore must be defined');

// 1. Setup initial local state (including a legacy tick = 1)
localStorage.setItem('ada-done', JSON.stringify(['ch0', 'ch1']));
localStorage.setItem('ada-ladder-v2', JSON.stringify({'98': 1, 'cf:659E': 2000, '200': 5000}));
localStorage.setItem('ada-deck', JSON.stringify({'q:s4:2': {n: 2, at: 3000}, 'q:s1:0': {n: 1, at: 1000}}));
localStorage.setItem('ada-endsem-date', '2026-11-28');

const exp = window.ADAStore.exportPayload();
assert(exp.app === 'ada-notebook', 'export app name must be ada-notebook');
assert(exp.schema === 1, 'export schema must be 1');
assert(typeof exp.exportedAt === 'string' && exp.exportedAt.includes('T'), 'exportedAt must be ISO timestamp');
assert(Array.isArray(exp.data['ada-done']) && exp.data['ada-done'].includes('ch0'), 'export includes ada-done');

// 2. Reject invalid JSON and wrong schema/app
const bad1 = window.ADAStore.validateImport('not json');
assert(!bad1.ok && bad1.error, 'rejects malformed json');

const bad2 = window.ADAStore.validateImport(JSON.stringify({app: 'other', schema: 1, data: {}}));
assert(!bad2.ok, 'rejects wrong app');

const bad3 = window.ADAStore.validateImport(JSON.stringify({app: 'ada-notebook', schema: 99, data: {}}));
assert(!bad3.ok, 'rejects wrong schema');

// 3. Merge rules (Review Focus #1 & #2):
// - '98' has local legacy tick (1 -> treated as 0), incoming has dated tick 1500 -> incoming wins (1500)
// - 'cf:659E' has local 2000, incoming has legacy 1 -> local 2000 wins
// - '200' has local 5000, incoming has 4000 -> local 5000 wins
// - 'cf:1418C' is new in incoming (6000) -> added
// - ada-done unions ['ch0', 'ch1'] with ['ch1', 'ch12', 'b0']
// - ada-deck merges by newest 'at'
const incoming = {
  app: 'ada-notebook',
  schema: 1,
  exportedAt: '2026-11-05T10:00:00.000Z',
  data: {
    'ada-done': ['ch1', 'ch12', 'b0'],
    'ada-ladder-v2': {'98': 1500, 'cf:659E': 1, '200': 4000, 'cf:1418C': 6000},
    'ada-deck': {'q:s4:2': {n: 1, at: 1000}, 'q:s1:0': {n: 4, at: 9000}, 'b:0:1': {n: 1, at: 2500}},
    'ada-endsem-date': '2026-12-02'
  }
};

const v = window.ADAStore.validateImport(JSON.stringify(incoming));
assert(v.ok, 'validates incoming payload');
assert(v.summary.newStops === 2, 'summary counts 2 new stops (ch12, b0), got ' + v.summary.newStops);
assert(v.summary.newProblems === 1, 'summary counts 1 new ladder solve (cf:1418C), got ' + v.summary.newProblems);
assert(v.summary.newMistakes === 1, 'summary counts 1 new mistake card (b:0:1), got ' + v.summary.newMistakes);

window.ADAStore.mergeImport(v.payload);

const doneAfter = JSON.parse(localStorage.getItem('ada-done'));
assert(doneAfter.length === 4 && doneAfter.includes('ch12') && doneAfter.includes('b0'), 'ada-done unioned');

const ladAfter = JSON.parse(localStorage.getItem('ada-ladder-v2'));
assert(ladAfter['98'] === 1500, 'dated tick beats legacy 1');
assert(ladAfter['cf:659E'] === 2000, 'newer local tick beats legacy 1');
assert(ladAfter['200'] === 5000, 'newer local tick beats older incoming');
assert(ladAfter['cf:1418C'] === 6000, 'new incoming problem added');

const deckAfter = JSON.parse(localStorage.getItem('ada-deck'));
assert(deckAfter['q:s4:2'].n === 2 && deckAfter['q:s4:2'].at === 3000, 'local newer mistake kept');
assert(deckAfter['q:s1:0'].n === 4 && deckAfter['q:s1:0'].at === 9000, 'incoming newer mistake wins');
assert(deckAfter['b:0:1'].n === 1, 'new incoming mistake added');

// 4. Verify [SYNC-1]: ada-ladder-star and ada-mock3 / ada-mock-lc merge even when local already initialized empty state
localStorage.setItem('ada-ladder-star', JSON.stringify({'98': 1}));
localStorage.setItem('ada-mock3', JSON.stringify({m1: {res: {'0': 0, '1': 1}}}));
localStorage.setItem('ada-mock-lc', JSON.stringify({lc1: {res: {'a': 0}}}));

const incoming2 = {
  app: 'ada-notebook',
  schema: 1,
  exportedAt: '2026-11-05T12:00:00.000Z',
  data: {
    'ada-ladder-star': {'cf:659E': 1},
    'ada-mock3': {m1: {res: {'0': 2, '1': 0, '2': 1}}, m2: {res: {'0': 3}}},
    'ada-mock-lc': {lc1: {res: {'a': 2}}}
  }
};
const v2 = window.ADAStore.validateImport(JSON.stringify(incoming2));
assert(v2.ok, 'validates incoming2 payload');
window.ADAStore.mergeImport(v2.payload);

const starAfter = JSON.parse(localStorage.getItem('ada-ladder-star'));
assert(starAfter['98'] === 1 && starAfter['cf:659E'] === 1, 'ada-ladder-star merged');

const mockAfter = JSON.parse(localStorage.getItem('ada-mock3'));
assert(mockAfter.m1.res['0'] === 2 && mockAfter.m1.res['1'] === 1 && mockAfter.m1.res['2'] === 1, 'ada-mock3 per-subtask max score merged');
assert(mockAfter.m2 && mockAfter.m2.res['0'] === 3, 'ada-mock3 new mock entry merged');

const lcAfter = JSON.parse(localStorage.getItem('ada-mock-lc'));
assert(lcAfter.lc1.res['a'] === 2, 'ada-mock-lc max score merged');

console.log('ALL STORE TESTS PASSED');
"""
    res = subprocess.run(['node', '-e', node_test, STORE_JS], capture_output=True, text=True)
    if res.returncode != 0:
        print(res.stdout)
        print(res.stderr)
        sys.exit(res.returncode)
    print(res.stdout.strip())

if __name__ == '__main__':
    main()

