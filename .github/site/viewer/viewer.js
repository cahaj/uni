/* File viewer, for pages written by viewer.py.

   The page holds only a shell. This script fetches the raw file named by
   #viewer[data-src], decodes it with the encoding found at build time, shows it
   with line numbers, and then loads highlight.js plus the one language file it
   needs from _viewer/ and swaps in the coloured version.

   - Click a line number to mark a line (#L12); Shift+click extends it to a range
     (#L12-L20). The marked lines are also opened and scrolled to from the URL.
   - "wrap" toggles line wrapping (remembered), "copy" copies the whole file.
   - Files over 500 KB, or with lines over 5000 characters, are shown uncoloured. */
(function () {
  'use strict';
  var host = document.getElementById('viewer');
  if (!host) return;

  var SRC = host.getAttribute('data-src');
  var ENC = host.getAttribute('data-enc') || 'utf-8';
  var LANG = host.getAttribute('data-lang') || '';
  var DEPS = (host.getAttribute('data-deps') || '').split(' ').filter(Boolean);
  var ROOT = host.getAttribute('data-root') || '';
  var SIZE = +host.getAttribute('data-size') || 0;
  var HIGHLIGHT_MAX_BYTES = 500 * 1024;
  var LONG_LINE = 5000;
  var BIG_FILE_LINES = 5000;

  var wrapBtn = document.getElementById('v-wrap');
  var copyBtn = document.getElementById('v-copy');
  var text = '';
  var lines = [];
  var code = null;
  var rowsEl = null;
  var current = null;   // marked line range [from, to] or null
  var anchorLine = null;
  var lit = [];

  /* ---- small helpers ---- */

  function esc(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  function splitLines(s) {
    var parts = s.split(/\r\n|\n|\r/);
    if (parts.length && parts[parts.length - 1] === '') parts.pop();
    return parts;
  }
  function loadScript(url) {
    return new Promise(function (ok, fail) {
      var el = document.createElement('script');
      el.src = url;
      el.onload = ok;
      el.onerror = function () { fail(new Error('could not load ' + url)); };
      document.head.appendChild(el);
    });
  }
  function status(message, rawLink) {
    var el = host.querySelector('.v-status') || host.appendChild(document.createElement('p'));
    el.className = 'v-status';
    el.textContent = message || '';
    if (rawLink) {
      var a = document.createElement('a');
      a.href = SRC;
      a.textContent = 'Open the raw file';
      el.appendChild(document.createTextNode(' '));
      el.appendChild(a);
      el.appendChild(document.createTextNode('.'));
    }
    el.hidden = !message;
  }

  /* ---- rendering ---- */

  function render(htmlLines) {
    var out = new Array(htmlLines.length);
    for (var i = 0; i < htmlLines.length; i++) {
      out[i] = '<div class="row" id="L' + (i + 1) + '"><span class="ln" data-n="' + (i + 1) +
               '"></span><span class="lc">' + htmlLines[i] + '</span></div>';
    }
    rowsEl.innerHTML = out.join('');
    lit = [];
    mark(current, false);
  }

  // highlight.js returns HTML whose <span>s can run across line breaks (block
  // comments, multi-line strings). Close them at each break and reopen them on the
  // next line so every line is self-contained.
  function splitHtml(htmlText) {
    var out = [], open = [], cur = '';
    var parts = htmlText.split(/(<span[^>]*>|<\/span>|\n)/);
    for (var i = 0; i < parts.length; i++) {
      var p = parts[i];
      if (p === '\n') {
        out.push(cur + new Array(open.length + 1).join('</span>'));
        cur = open.join('');
      } else if (p === '</span>') {
        open.pop();
        cur += p;
      } else {
        if (p.indexOf('<span') === 0) open.push(p);
        cur += p;
      }
    }
    out.push(cur);
    return out;
  }

  function highlight() {
    if (!LANG || SIZE > HIGHLIGHT_MAX_BYTES) return;
    for (var i = 0; i < lines.length; i++) if (lines[i].length > LONG_LINE) return;
    var base = ROOT + '_viewer/';
    loadScript(base + 'hljs.js')
      .then(function () { return loadScript(base + 'langs/' + LANG + '.js'); })
      .then(function () {
        // embedded languages (CSS/JS inside HTML) are a bonus: ignore failures
        return Promise.all(DEPS.map(function (d) {
          return loadScript(base + 'langs/' + d + '.js').catch(function () {});
        }));
      })
      .then(function () {
        var res = window.hljs.highlight(lines.join('\n'), { language: LANG, ignoreIllegals: true });
        var coloured = splitHtml(res.value);
        if (coloured.length === lines.length) render(coloured);
      })
      .catch(function () { /* stay uncoloured */ });
  }

  /* ---- marked lines ---- */

  function parseHash() {
    var m = /^#L(\d+)(?:-L?(\d+))?$/.exec(location.hash);
    if (!m) return null;
    var a = +m[1], b = m[2] ? +m[2] : a;
    if (a > b) { var t = a; a = b; b = t; }
    if (a < 1 || a > lines.length) return null;
    return [a, Math.min(b, lines.length)];
  }
  function mark(range, scroll) {
    for (var i = 0; i < lit.length; i++) lit[i].classList.remove('hl');
    lit = [];
    if (!range) return;
    for (var n = range[0]; n <= range[1]; n++) {
      var row = document.getElementById('L' + n);
      if (row) { row.classList.add('hl'); lit.push(row); }
    }
    if (scroll && lit[0]) lit[0].scrollIntoView({ block: 'center' });
  }
  function setHash(range) {
    var url = location.pathname + location.search;
    if (range) url += '#L' + range[0] + (range[1] > range[0] ? '-L' + range[1] : '');
    history.replaceState(null, '', url);
  }

  function onLineClick(e) {
    var ln = e.target.closest && e.target.closest('.ln');
    if (!ln) return;
    var n = +ln.getAttribute('data-n');
    var range;
    if (e.shiftKey && anchorLine) {
      range = [Math.min(anchorLine, n), Math.max(anchorLine, n)];
    } else if (current && current[0] === n && current[1] === n) {
      range = null;                      // clicking the marked line again clears it
    } else {
      anchorLine = n;
      range = [n, n];
    }
    current = range;
    mark(range, false);
    setHash(range);
  }

  /* ---- wrap and copy ---- */

  function wrapPref() {
    try { return localStorage.getItem('viewer.wrap') === '1'; } catch (e) { return false; }
  }
  function setWrap(on, remember) {
    wrapBtn.setAttribute('aria-pressed', on ? 'true' : 'false');
    if (code) code.classList.toggle('wrap', on);
    if (remember) { try { localStorage.setItem('viewer.wrap', on ? '1' : '0'); } catch (e) { /* ignore */ } }
  }
  function copyText(s) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(s);
    return new Promise(function (ok, no) {
      var ta = document.createElement('textarea');
      ta.value = s;
      ta.setAttribute('readonly', '');
      ta.style.cssText = 'position:fixed;opacity:0';
      document.body.appendChild(ta);
      ta.select();
      var good = false;
      try { good = document.execCommand('copy'); } catch (e) { /* ignore */ }
      document.body.removeChild(ta);
      if (good) ok(); else no();
    });
  }
  function flash(button, message) {
    var old = button.getAttribute('data-label') || button.textContent;
    button.setAttribute('data-label', old);
    button.textContent = message;
    setTimeout(function () { button.textContent = old; }, 1500);
  }

  wrapBtn.addEventListener('click', function () {
    setWrap(wrapBtn.getAttribute('aria-pressed') !== 'true', true);
  });
  copyBtn.addEventListener('click', function () {
    if (!lines.length) return;
    copyText(text).then(function () { flash(copyBtn, 'copied'); },
                        function () { flash(copyBtn, 'copy failed'); });
  });
  setWrap(wrapPref(), false);

  /* ---- load ---- */

  var slow = setTimeout(function () { status('Loading\u2026'); }, 250);

  function failed(message) {
    clearTimeout(slow);
    if (location.protocol === 'file:') {
      message = 'Browsers do not let a page read files when it is opened from disk. ' +
                'Serve the folder (for example python3 -m http.server) or open the published site.';
    }
    status(message, true);
  }

  host.setAttribute('aria-busy', 'true');
  fetch(SRC).then(function (response) {
    if (!response.ok) throw new Error('HTTP ' + response.status);
    return response.arrayBuffer();
  }).then(function (buffer) {
    try { text = new TextDecoder(ENC).decode(buffer); }
    catch (e) { text = new TextDecoder('utf-8').decode(buffer); }
    lines = splitLines(text);
    clearTimeout(slow);
    host.removeAttribute('aria-busy');
    if (!lines.length) { status('This file is empty.'); return; }
    status('');

    code = document.createElement('div');
    code.className = 'code' + (lines.length > BIG_FILE_LINES ? ' big' : '');
    code.style.setProperty('--digits', String(String(lines.length).length));
    rowsEl = document.createElement('div');
    rowsEl.className = 'rows';
    code.appendChild(rowsEl);
    host.appendChild(code);
    setWrap(wrapBtn.getAttribute('aria-pressed') === 'true', false);
    rowsEl.addEventListener('click', onLineClick);

    current = parseHash();
    if (current) anchorLine = current[0];
    render(lines.map(esc));
    mark(current, true);
    window.addEventListener('hashchange', function () {
      current = parseHash();
      if (current) anchorLine = current[0];
      mark(current, true);
    });

    // paint the plain text first, then colour it
    requestAnimationFrame(function () { setTimeout(highlight, 0); });
  }).catch(function (err) {
    failed('Could not load the file (' + err.message + ').');
  });
})();
