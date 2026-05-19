/* writeup_detail.js — Reading progress, TOC, terminal code blocks, copy button */
(function () {
  'use strict';

  /* Scroll to top on load */
  window.scrollTo(0, 0);

  /* ── Syntax highlighting ── */
  function initHighlight() {
    if (typeof hljs === 'undefined') return;
    document.querySelectorAll('#writeup-body pre code').forEach(function (el) {
      hljs.highlightElement(el);
    });
  }

  /* ── Terminal-style code block wrappers ── */
  function initTerminals() {
    var body = document.getElementById('writeup-body');
    if (!body) return;

    body.querySelectorAll('pre').forEach(function (pre) {
      var code = pre.querySelector('code');
      if (!code) return;

      /* Detect language from class */
      var langClass = Array.from(code.classList).find(function (c) {
        return c.startsWith('language-') || c.startsWith('lang-');
      });
      var lang = langClass
        ? langClass.replace('language-', '').replace('lang-', '')
        : 'code';

      var isTerminal = ['bash', 'sh', 'shell', 'zsh', 'powershell'].indexOf(lang) !== -1;
      var promptLabel = isTerminal ? 'kali@kali:~$' : lang;

      /* Build wrapper */
      var wrapper = document.createElement('div');
      wrapper.className = 'wu-terminal';

      var header = document.createElement('div');
      header.className = 'wu-term-header';
      header.innerHTML =
        '<span class="wu-term-dot r"></span>' +
        '<span class="wu-term-dot y"></span>' +
        '<span class="wu-term-dot g"></span>' +
        '<span class="wu-term-prompt">' + escHtml(promptLabel) + '</span>' +
        '<span class="wu-term-lang">' + escHtml(lang.toUpperCase()) + '</span>' +
        '<button class="wu-copy-btn" type="button">Copy</button>';

      pre.parentNode.insertBefore(wrapper, pre);
      wrapper.appendChild(header);
      wrapper.appendChild(pre);

      /* Copy button */
      var btn = header.querySelector('.wu-copy-btn');
      btn.addEventListener('click', function () {
        var text = code.textContent || '';
        copyText(text, btn);
      });
    });
  }

  function copyText(text, btn) {
    function showCopied() {
      btn.textContent = 'Copied!';
      btn.classList.add('wu-copied');
      setTimeout(function () {
        btn.textContent = 'Copy';
        btn.classList.remove('wu-copied');
      }, 2000);
    }

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(showCopied).catch(fallbackCopy);
    } else {
      fallbackCopy();
    }

    function fallbackCopy() {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.style.cssText = 'position:fixed;opacity:0;top:0;left:0;';
      document.body.appendChild(ta);
      ta.focus();
      ta.select();
      try { document.execCommand('copy'); showCopied(); } catch (_) { /* silent fail */ }
      document.body.removeChild(ta);
    }
  }

  function escHtml(str) {
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  /* ── Table of Contents ── */
  function initTOC() {
    var body = document.getElementById('writeup-body');
    var tocNav = document.getElementById('wu-toc-nav');
    if (!body || !tocNav) return;

    var headings = body.querySelectorAll('h2, h3');
    if (headings.length === 0) {
      tocNav.innerHTML = '<p class="wu-toc-loading">No sections</p>';
      return;
    }

    tocNav.innerHTML = '';
    headings.forEach(function (h, i) {
      var id = 'wu-h-' + i;
      h.id = id;

      var a = document.createElement('a');
      a.href = '#' + id;
      a.textContent = h.textContent.trim();
      a.className = h.tagName === 'H3' ? 'toc-h3' : 'toc-h2';

      a.addEventListener('click', function (e) {
        e.preventDefault();
        var offset = 80;
        var top = h.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top: top, behavior: 'smooth' });
      });

      tocNav.appendChild(a);
    });

    /* Highlight active section on scroll */
    var tocLinks = tocNav.querySelectorAll('a');
    var headingArr = Array.from(headings);

    function onScroll() {
      var scrollY = window.scrollY + 100;
      var active = null;
      headingArr.forEach(function (h, i) {
        if (h.offsetTop <= scrollY) active = i;
      });
      tocLinks.forEach(function (a, i) {
        a.classList.toggle('toc-active', i === active);
      });
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ── Reading Progress Bar ── */
  function initProgressBar() {
    var bar = document.getElementById('wu-progress');
    if (!bar) return;

    function update() {
      var doc = document.documentElement;
      var total = doc.scrollHeight - doc.clientHeight;
      var pct = total > 0 ? (window.scrollY / total) * 100 : 0;
      bar.style.width = Math.min(pct, 100) + '%';
    }

    window.addEventListener('scroll', update, { passive: true });
    update();
  }

  /* ── Init ── */
  document.addEventListener('DOMContentLoaded', function () {
    initHighlight();
    initTerminals();
    initTOC();
    initProgressBar();
  });
}());
