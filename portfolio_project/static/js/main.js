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
  }

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
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
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

});
