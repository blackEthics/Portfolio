/* ── carousel.js ── Generic carousel (reserved for future use) ── */

(function () {
  function initCarousel(wrapper) {
    var track = wrapper.querySelector('.carousel-track');
    var prevBtn = wrapper.querySelector('.carousel-prev');
    var nextBtn = wrapper.querySelector('.carousel-next');
    if (!track) return;

    var current = 0;
    var items = track.children;

    function goTo(index) {
      var count = items.length;
      current = (index + count) % count;
      track.style.transform = 'translateX(-' + (current * 100) + '%)';
    }

    if (prevBtn) prevBtn.addEventListener('click', function () { goTo(current - 1); });
    if (nextBtn) nextBtn.addEventListener('click', function () { goTo(current + 1); });
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-carousel]').forEach(initCarousel);
  });
})();
