/* ── main.js ── Core UI behaviours ── */

document.addEventListener('DOMContentLoaded', function () {

  // ── Loading screen ──
  var loadingScreen = document.getElementById('loading-screen');
  if (loadingScreen) {
    setTimeout(function () {
      loadingScreen.classList.add('hidden');
      setTimeout(function () { loadingScreen.remove(); }, 400);
    }, 1200);
  }

  // ── Hamburger / mobile menu ──
  var hamburger = document.getElementById('hamburger');
  var mobileMenu = document.getElementById('mobile-menu');
  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', function () {
      hamburger.classList.toggle('open');
      mobileMenu.classList.toggle('open');
    });
    document.querySelectorAll('.mobile-link').forEach(function (link) {
      link.addEventListener('click', function () {
        hamburger.classList.remove('open');
        mobileMenu.classList.remove('open');
      });
    });
    // Close menu when clicking outside
    document.addEventListener('click', function (e) {
      if (mobileMenu.classList.contains('open') &&
          !mobileMenu.contains(e.target) &&
          !hamburger.contains(e.target)) {
        hamburger.classList.remove('open');
        mobileMenu.classList.remove('open');
      }
    });
    // Close menu on resize above breakpoint
    window.addEventListener('resize', function () {
      if (window.innerWidth > 1100) {
        hamburger.classList.remove('open');
        mobileMenu.classList.remove('open');
      }
    }, { passive: true });
  }

  // ── Scrollspy + sliding indicator ──
  var spySections  = Array.from(document.querySelectorAll('section[id]'));
  var spyLinks     = document.querySelectorAll('.nav-links a');
  var navIndicator = document.getElementById('nav-indicator');
  var navWrap      = document.getElementById('nav-links-wrap');

  function positionIndicator(linkEl) {
    if (!navIndicator || !navWrap || !linkEl) return;
    // Walk the offsetParent chain from the link up to navWrap
    var left = 0, node = linkEl;
    while (node && node !== navWrap) {
      left += node.offsetLeft;
      node = node.offsetParent;
    }
    var width = linkEl.offsetWidth;
    if (!width) return;
    navIndicator.style.left    = left + 'px';
    navIndicator.style.width   = width + 'px';
    navIndicator.style.opacity = '1';
  }

  function setActiveNav(id) {
    var activeLink = null;
    spyLinks.forEach(function (a) {
      var href = a.getAttribute('href') || '';
      var isActive = href === '#' + id || href.endsWith('#' + id);
      a.classList.toggle('active', isActive);
      if (isActive) activeLink = a;
    });
    if (activeLink) positionIndicator(activeLink);

    // Mirror active state onto mobile menu links
    document.querySelectorAll('.mobile-link').forEach(function (a) {
      var href = a.getAttribute('href') || '';
      a.classList.toggle('active', href === '#' + id || href.endsWith('#' + id));
    });
  }

  function findActiveSection() {
    var scrollY = window.scrollY + 120;
    var active  = spySections[0] ? spySections[0].id : null;
    for (var i = 0; i < spySections.length; i++) {
      if (spySections[i].offsetTop <= scrollY) active = spySections[i].id;
    }
    return active;
  }

  function initScrollSpy() {
    setActiveNav(findActiveSection());
  }

  if (spySections.length && spyLinks.length) {
    // Staggered init: catches layout, font-load, and post-loading-screen states
    requestAnimationFrame(function () { requestAnimationFrame(initScrollSpy); });
    setTimeout(initScrollSpy, 100);
    setTimeout(initScrollSpy, 500);
    setTimeout(initScrollSpy, 1700); // after loading screen fades (1200ms + 400ms fade)
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(initScrollSpy);
    window.addEventListener('load', initScrollSpy, { once: true });

    window.addEventListener('scroll', function () { setActiveNav(findActiveSection()); }, { passive: true });
    window.addEventListener('resize', function () {
      var cur = document.querySelector('.nav-links a.active');
      if (cur) positionIndicator(cur);
    }, { passive: true });
  }

  // Clicking a link snaps the indicator immediately before scroll settles
  spyLinks.forEach(function (a) {
    a.addEventListener('click', function () { positionIndicator(this); });
  });

  // ── Back to top ──
  var backTop = document.getElementById('back-top');
  if (backTop) {
    window.addEventListener('scroll', function () {
      backTop.classList.toggle('show', window.scrollY > 300);
    });
  }

  // ── Smooth scroll for anchor links ──
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href').slice(1);
      var target = document.getElementById(id);
      if (target) {
        e.preventDefault();
        var navbar = document.getElementById('navbar');
        var offset = navbar ? navbar.offsetHeight + 8 : 80;
        var top = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top: top, behavior: 'smooth' });
      }
    });
  });

  // ── Contact form success banner auto-hide ──
  var banner = document.getElementById('form-success-banner');
  if (banner) {
    setTimeout(function () {
      banner.style.transition = 'opacity 0.4s';
      banner.style.opacity = '0';
      setTimeout(function () { banner.remove(); }, 400);
    }, 5000);
  }

  // ── Footer terminal sequential reveal ──
  var cftTerminal = document.getElementById('cft-terminal');
  if (cftTerminal) {
    var cftRows = cftTerminal.querySelectorAll('.cft-row');
    cftRows.forEach(function (row, i) {
      row.style.setProperty('--d', (i * 0.11) + 's');
    });
    var cftObserver = new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting) {
        cftTerminal.classList.add('cft-visible');
        cftObserver.disconnect();
      }
    }, { threshold: 0.15 });
    cftObserver.observe(cftTerminal);
  }

});
