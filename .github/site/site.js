/* One small script shared by every generated page. Each section below does
   nothing unless the elements it needs are on the page:

   1. Directory listing: keyboard navigation.
   2. Rendered markdown (also a README under a listing): collapsible headings.
   3. Rendered markdown pages and file-viewer pages: keyboard access to the
      "Directory" and "raw" links.

   Keys pressed together with Shift/Ctrl/Alt/Meta are always ignored, so browser
   shortcuts keep working. */
(function () {
  'use strict';

  /* ---- shared helpers ---- */

  // When a key jumps the page to the top (so the selected item is visible), the
  // old reading position is remembered; Escape returns to it if the page is
  // still at the top.
  var savedY = null;
  function jumpTop() {
    if (savedY === null && window.scrollY > 0) savedY = window.scrollY;
    window.scrollTo(0, 0);
  }
  function restoreScroll() {
    if (savedY !== null && window.scrollY < 5) window.scrollTo(0, savedY);
    savedY = null;
  }
  function plainKey(e) {
    return !(e.defaultPrevented || e.shiftKey || e.ctrlKey || e.altKey || e.metaKey);
  }
  function typing(t) {
    return !!t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName));
  }

  /* ---- 1. Directory listing: keyboard navigation ----
     The page behaves normally until Up or Down is pressed. That selects the
     first row; from then on Up/Down move the selection (no wrap-around), Enter
     opens the row's main link and Escape clears the selection, handing the
     arrow keys back to the browser. The selected row's link really has focus,
     so Enter, Tab, Ctrl/Cmd+Enter (new tab) and screen readers work natively;
     Tab-ing to a link marks its row too. */
  (function () {
    var table = document.querySelector('table.files');
    if (!table || !table.rows.length) return;
    var rows = Array.prototype.slice.call(table.rows);
    var cur = -1;

    function mainLink(row) { return row.querySelector('td.name a'); }

    function select(i, focus) {
      if (cur >= 0) rows[cur].classList.remove('sel');
      cur = i;
      if (i < 0) return;
      var row = rows[i];
      row.classList.add('sel');
      if (focus) {
        var a = mainLink(row);
        if (a) a.focus({ preventScroll: true });
      }
      if (i === 0) jumpTop();
      else row.scrollIntoView({ block: 'nearest' });
    }

    document.addEventListener('keydown', function (e) {
      if (!plainKey(e) || typing(e.target)) return;
      var t = e.target;

      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        if (cur < 0) { select(0, true); return; }
        var next = cur + (e.key === 'ArrowDown' ? 1 : -1);
        select(Math.max(0, Math.min(rows.length - 1, next)), true);
      } else if (e.key === 'Escape' && cur >= 0) {
        var active = document.activeElement;
        if (active && table.contains(active)) active.blur();
        select(-1);
        restoreScroll();
      } else if (e.key === 'Enter' && cur >= 0 && !(t.closest && t.closest('table.files a'))) {
        var a = mainLink(rows[cur]);
        if (a) { e.preventDefault(); a.click(); }
      }
    });

    table.addEventListener('focusin', function (e) {
      var i = rows.indexOf(e.target.closest('tr'));
      if (i >= 0 && i !== cur && e.target.matches(':focus-visible')) select(i, false);
    });
    table.addEventListener('focusout', function (e) {
      if (!e.relatedTarget || !table.contains(e.relatedTarget)) select(-1);
    });
  })();

  /* ---- 2. Collapsible headings ----
     A heading with content below it gets a chevron button. Clicking the
     heading (or pressing Enter/Space on the button) hides everything up to the
     next heading of the same or a higher level, including nested sections,
     whose own collapsed state is kept. Following a link to something inside a
     collapsed section (a TOC entry, a #hash in the URL) opens it. Without
     JavaScript the page is simply fully expanded. */
  (function () {
    var article = document.querySelector('article.md');
    if (!article) return;
    var kids = Array.prototype.slice.call(article.children);

    function level(el) {
      var m = /^H([1-6])$/.exec(el.tagName);
      return m ? +m[1] : 0;
    }
    function isCollapsed(h) { return h.classList.contains('collapsed'); }
    function setCollapsed(h, v) {
      h.classList.toggle('collapsed', v);
      h.querySelector('.chev-btn').setAttribute('aria-expanded', v ? 'false' : 'true');
    }

    kids.forEach(function (el, i) {
      var lvl = level(el);
      if (!lvl) return;
      var next = kids[i + 1];
      if (!next || (level(next) && level(next) <= lvl)) return; // nothing to collapse
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'chev-btn';
      btn.setAttribute('aria-expanded', 'true');
      btn.setAttribute('aria-label', 'Toggle section');
      btn.innerHTML = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>';
      el.insertBefore(btn, el.firstChild);
      el.classList.add('collapsible');
    });

    // Hide every element that sits inside a collapsed section.
    function apply() {
      var closedAt = Infinity; // level of the collapsed heading we are inside
      kids.forEach(function (el) {
        var lvl = level(el);
        if (lvl && lvl <= closedAt) closedAt = Infinity; // left that section
        el.hidden = closedAt !== Infinity;
        if (lvl && closedAt === Infinity && isCollapsed(el)) closedAt = lvl;
      });
    }

    article.addEventListener('click', function (e) {
      var h = e.target.closest('.collapsible');
      if (!h || h.parentNode !== article) return;
      if (e.target.closest('a') || e.detail > 1 || String(window.getSelection())) return;
      setCollapsed(h, !isCollapsed(h));
      apply();
    });

    // Open whatever hides the element the URL hash points at.
    function reveal(el) {
      var sec = el;
      while (sec && sec.parentNode !== article) sec = sec.parentNode;
      if (!sec) return false;
      var changed = false;
      var need = level(sec) || 7;
      if (level(sec) && isCollapsed(sec)) { setCollapsed(sec, false); changed = true; }
      for (var j = kids.indexOf(sec) - 1; j >= 0; j--) {
        var l = level(kids[j]);
        if (l && l < need) {
          need = l;
          if (isCollapsed(kids[j])) { setCollapsed(kids[j], false); changed = true; }
        }
      }
      if (changed) apply();
      return changed;
    }
    function onHash() {
      var id = location.hash.slice(1);
      try { id = decodeURIComponent(id); } catch (err) { /* keep raw id */ }
      var el = id && document.getElementById(id);
      if (el && article.contains(el) && reveal(el)) el.scrollIntoView();
    }
    window.addEventListener('hashchange', onHash);
    onHash();
  })();

  /* ---- 3. Rendered markdown page: "Directory" / "raw" from the keyboard ----
     Left selects Directory, Right selects raw (the link gets focus, so Enter
     opens it) and Escape deselects, like in the directory listing. */
  (function () {
    var nav = document.querySelector('.meta-inline');
    var dirLink = nav && nav.querySelector('a.nav-dir');
    var rawLink = nav && nav.querySelector('a.nav-raw');
    if (!dirLink || !rawLink) return;

    document.addEventListener('keydown', function (e) {
      if (!plainKey(e) || typing(e.target)) return;
      // leave code blocks, tables and the file viewer alone while they scroll sideways
      var box = e.target.closest && e.target.closest('pre, table, .code');
      if (box && box.scrollWidth > box.clientWidth) return;

      if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
        e.preventDefault();
        jumpTop();
        (e.key === 'ArrowLeft' ? dirLink : rawLink).focus({ preventScroll: true });
      } else if (e.key === 'Escape') {
        var a = document.activeElement;
        if (a === dirLink || a === rawLink) { a.blur(); restoreScroll(); }
      }
    });
  })();
})();
