/* ===== ADAStore: Portable Progress, Export / Import & Merge Engine (Roadmap P1/P3) ===== */
(function () {
  var KEYS = [
    'ada-done',
    'ada-ladder-v2',
    'ada-deck',
    'ada-mock',
    'ada-mock3',
    'ada-mock-lc',
    'ada-endsem-date',
    'ada-quick',
    'ada-theme2'
  ];

  function safeParse(str, fallback) {
    if (str == null || str === '') return fallback;
    try {
      return JSON.parse(str);
    } catch (_) {
      return fallback;
    }
  }

  function readRawKey(k) {
    try {
      return localStorage.getItem(k);
    } catch (_) {
      return null;
    }
  }

  function writeKey(k, val) {
    try {
      if (typeof val === 'string') localStorage.setItem(k, val);
      else localStorage.setItem(k, JSON.stringify(val));
    } catch (_) {}
  }

  function normalizeTickTime(v) {
    if (v === 1 || v === '1' || v === true) return 0;
    var n = Number(v);
    return Number.isFinite(n) && n > 0 ? n : 0;
  }

  function exportPayload() {
    var data = {};
    var done = safeParse(readRawKey('ada-done'), []);
    data['ada-done'] = Array.isArray(done) ? done : [];
    data['ada-ladder-v2'] = safeParse(readRawKey('ada-ladder-v2'), {}) || {};
    data['ada-deck'] = safeParse(readRawKey('ada-deck'), {}) || {};

    var mock3 = safeParse(readRawKey('ada-mock3'), null);
    if (mock3) data['ada-mock3'] = mock3;

    var mockLc = safeParse(readRawKey('ada-mock-lc'), null);
    if (mockLc) data['ada-mock-lc'] = mockLc;

    var endsem = readRawKey('ada-endsem-date');
    if (endsem) {
      var parsedDate = safeParse(endsem, endsem);
      data['ada-endsem-date'] = parsedDate;
    }

    var quick = readRawKey('ada-quick');
    if (quick != null) data['ada-quick'] = safeParse(quick, quick);

    var theme = readRawKey('ada-theme2');
    if (theme != null) data['ada-theme2'] = safeParse(theme, theme);

    return {
      app: 'ada-notebook',
      schema: 1,
      exportedAt: new Date().toISOString(),
      data: data
    };
  }

  function computeSummary(incomingData) {
    var curDone = new Set(safeParse(readRawKey('ada-done'), []) || []);
    var inDone = Array.isArray(incomingData['ada-done']) ? incomingData['ada-done'] : [];
    var newStops = 0;
    inDone.forEach(function (id) {
      if (typeof id === 'string' && !curDone.has(id)) newStops++;
    });

    var curLad = safeParse(readRawKey('ada-ladder-v2'), {}) || {};
    var inLad = incomingData['ada-ladder-v2'] && typeof incomingData['ada-ladder-v2'] === 'object' ? incomingData['ada-ladder-v2'] : {};
    var newProblems = 0;
    Object.keys(inLad).forEach(function (k) {
      if (inLad[k] != null && !Object.prototype.hasOwnProperty.call(curLad, k)) newProblems++;
    });

    var curDeck = safeParse(readRawKey('ada-deck'), {}) || {};
    var inDeck = incomingData['ada-deck'] && typeof incomingData['ada-deck'] === 'object' ? incomingData['ada-deck'] : {};
    var newMistakes = 0;
    Object.keys(inDeck).forEach(function (k) {
      if (inDeck[k] != null && !Object.prototype.hasOwnProperty.call(curDeck, k)) newMistakes++;
    });

    return {
      newStops: newStops,
      newProblems: newProblems,
      newMistakes: newMistakes,
      totalStopsIncoming: inDone.length,
      totalProblemsIncoming: Object.keys(inLad).length,
      totalMistakesIncoming: Object.keys(inDeck).length
    };
  }

  function validateImport(rawText) {
    if (typeof rawText !== 'string' || !rawText.trim()) {
      return { ok: false, error: 'Empty file or input.' };
    }
    var obj;
    try {
      obj = JSON.parse(rawText);
    } catch (e) {
      return { ok: false, error: 'Invalid JSON file: ' + e.message };
    }
    if (!obj || typeof obj !== 'object') {
      return { ok: false, error: 'Root JSON value must be an object.' };
    }
    if (obj.app !== 'ada-notebook') {
      return { ok: false, error: 'Refused: expected app "ada-notebook", got "' + String(obj.app) + '".' };
    }
    if (obj.schema !== 1) {
      return { ok: false, error: 'Refused: unsupported schema version "' + String(obj.schema) + '" (expected 1).' };
    }
    if (!obj.data || typeof obj.data !== 'object') {
      return { ok: false, error: 'Missing "data" object in export payload.' };
    }
    return {
      ok: true,
      payload: obj,
      summary: computeSummary(obj.data)
    };
  }

  function mergeImport(payload) {
    if (!payload || payload.app !== 'ada-notebook' || payload.schema !== 1 || !payload.data) {
      throw new Error('Invalid payload passed to mergeImport');
    }
    var d = payload.data;

    // 1. Merge ada-done (set union preserving order)
    var curDone = safeParse(readRawKey('ada-done'), []);
    if (!Array.isArray(curDone)) curDone = [];
    var seenDone = new Set(curDone);
    if (Array.isArray(d['ada-done'])) {
      d['ada-done'].forEach(function (id) {
        if (typeof id === 'string' && !seenDone.has(id)) {
          seenDone.add(id);
          curDone.push(id);
        }
      });
    }
    writeKey('ada-done', curDone);

    // 2. Merge ada-ladder-v2 (map key -> timestamp; legacy 1 treated as 0; newest wins)
    var curLad = safeParse(readRawKey('ada-ladder-v2'), {});
    if (!curLad || typeof curLad !== 'object') curLad = {};
    var inLad = d['ada-ladder-v2'];
    if (inLad && typeof inLad === 'object') {
      Object.keys(inLad).forEach(function (k) {
        var inVal = inLad[k];
        if (inVal == null) return;
        if (!Object.prototype.hasOwnProperty.call(curLad, k)) {
          curLad[k] = inVal;
        } else {
          var tCur = normalizeTickTime(curLad[k]);
          var tIn = normalizeTickTime(inVal);
          if (tIn > tCur) {
            curLad[k] = inVal;
          }
        }
      });
    }
    writeKey('ada-ladder-v2', curLad);

    // 3. Merge ada-deck (counter map key -> {n, at}; newest 'at' wins)
    var curDeck = safeParse(readRawKey('ada-deck'), {});
    if (!curDeck || typeof curDeck !== 'object') curDeck = {};
    var inDeck = d['ada-deck'];
    if (inDeck && typeof inDeck === 'object') {
      Object.keys(inDeck).forEach(function (k) {
        var inItem = inDeck[k];
        if (!inItem || typeof inItem !== 'object') return;
        var curItem = curDeck[k];
        if (!curItem || typeof curItem !== 'object') {
          curDeck[k] = { n: Number(inItem.n) || 1, at: Number(inItem.at) || 0 };
        } else {
          var atCur = Number(curItem.at) || 0;
          var atIn = Number(inItem.at) || 0;
          if (atIn > atCur) {
            curDeck[k] = { n: Number(inItem.n) || 1, at: atIn };
          }
        }
      });
    }
    writeKey('ada-deck', curDeck);

    // 4. Optional single-value / mock keys
    if (d['ada-mock3'] && !readRawKey('ada-mock3')) {
      writeKey('ada-mock3', d['ada-mock3']);
    }
    if (d['ada-mock-lc'] && !readRawKey('ada-mock-lc')) {
      writeKey('ada-mock-lc', d['ada-mock-lc']);
    }
    if (typeof d['ada-endsem-date'] === 'string' && d['ada-endsem-date']) {
      writeKey('ada-endsem-date', d['ada-endsem-date']);
    }

    writeKey('ada-last-export', new Date().toISOString());
    return computeSummary(d);
  }

  function downloadExport() {
    var payload = exportPayload();
    var json = JSON.stringify(payload, null, 2);
    writeKey('ada-last-export', payload.exportedAt);
    if (typeof Blob !== 'undefined' && typeof URL !== 'undefined' && document.createElement) {
      var blob = new Blob([json], { type: 'application/json' });
      var url = URL.createObjectURL(blob);
      var a = document.createElement('a');
      var dateStr = payload.exportedAt.slice(0, 10);
      a.href = url;
      a.download = 'ada-notebook-progress-' + dateStr + '.json';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
    }
    return payload;
  }

  function lastExportStatus() {
    var raw = readRawKey('ada-last-export');
    if (!raw) return { never: true, days: null, label: 'Not backed up yet' };
    var t = Date.parse(raw);
    if (!Number.isFinite(t)) return { never: true, days: null, label: 'Not backed up yet' };
    var days = Math.max(0, Math.floor((Date.now() - t) / 86400000));
    return {
      never: false,
      days: days,
      label: days === 0 ? 'Backed up today' : ('Last exported ' + days + (days === 1 ? ' day ago' : ' days ago'))
    };
  }

  window.ADAStore = {
    KEYS: KEYS,
    exportPayload: exportPayload,
    validateImport: validateImport,
    mergeImport: mergeImport,
    downloadExport: downloadExport,
    lastExportStatus: lastExportStatus
  };
})();
