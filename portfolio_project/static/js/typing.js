/* ── typing.js ── Typewriter animation ── */

document.addEventListener('DOMContentLoaded', function () {
  var el = document.getElementById('typewriter-text');
  if (!el) return;

  var roles = ['Vulnerability Assessment', 'Penetration Tester', 'Cybersecurity Engineer'];

  var rolesEl = document.getElementById('typewriter-roles');
  if (rolesEl) {
    try {
      var parsed = JSON.parse(rolesEl.textContent);
      if (Array.isArray(parsed) && parsed.length) roles = parsed;
    } catch (e) {}
  }

  var rIdx = 0, cIdx = 0, deleting = false;

  function tick() {
    var current = roles[rIdx];

    if (!deleting) {
      cIdx++;
      el.textContent = current.slice(0, cIdx);
      if (cIdx === current.length) {
        deleting = true;
        setTimeout(tick, 2200);
        return;
      }
      setTimeout(tick, 75 + Math.random() * 40);
    } else {
      cIdx--;
      el.textContent = current.slice(0, cIdx);
      if (cIdx === 0) {
        deleting = false;
        rIdx = (rIdx + 1) % roles.length;
        setTimeout(tick, 380);
        return;
      }
      setTimeout(tick, 38 + Math.random() * 18);
    }
  }

  setTimeout(tick, 500);
});
