/* ===== v4: exam-practice items, appended so saved ids (q:key:index, b:index, g:index) never move ===== */
(function () {
  'use strict';
  const D = __V4_DATA__;
  Object.entries(D.quiz).forEach(([k, arr]) => { if (!QUIZ[k]) QUIZ[k] = []; arr.forEach(q => QUIZ[k].push(q)); });
  D.extra.forEach(q => EXTRA_QS.push(q));
  D.blanks.forEach(b => BLANKS.push(b));
  D.bugs.forEach(b => BUGS.push(b));
  D.parsons.forEach(b => PARSONS.push(b));
  Object.assign(TOPIC_NAMES, D.names);
  Object.assign(window.SECMAP, D.secmap);
})();
