/* background.js — Matrix rain + floating code particles */
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var canvas = document.getElementById('bg-canvas');
  if (!canvas) return;
  var ctx = canvas.getContext('2d');

  var W = 0, H = 0;
  var FONT = 13;
  var TRAIL = 18;
  var cols, drops, speeds, colType;

  var CHARS = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモ{}[]<>|/\\#@!$%^&*;:=+01234567890xABCDEFabcdef';

  function initMatrix() {
    cols = Math.floor(W / FONT);
    drops = [];
    speeds = [];
    colType = [];
    for (var i = 0; i < cols; i++) {
      drops.push(-Math.floor(Math.random() * 80));
      speeds.push(0.2 + Math.random() * 0.65);
      var r = Math.random();
      colType.push(r > 0.92 ? 'red' : r > 0.82 ? 'cyan' : 'green');
    }
  }

  function resize() {
    W = canvas.width = window.innerWidth;
    H = canvas.height = window.innerHeight;
    initMatrix();
  }

  /* Floating code snippets */
  var SNIPPETS = [
    'nmap -sV', 'root@kali:~#', '0x41414141', 'CVE-2024-1234', 'XSS',
    'SQLI', 'reverse_shell.py', '#!/bin/bash', '/bin/sh -i', 'sudo -l',
    'msfconsole', 'hashcat -m', '0xDEADBEEF', 'PAYLOAD', 'exploit.py',
    '10.10.10.1', 'netstat -an', 'sqlmap -u', 'gobuster dir', 'nikto -h',
    'hydra -l', 'john --wordlist', 'nc -lvnp', 'chmod +x', 'whoami'
  ];

  var particles = [];
  for (var p = 0; p < 24; p++) {
    particles.push({
      x: Math.random() * 1920,
      y: Math.random() * 1080,
      vx: (Math.random() - 0.5) * 0.3,
      vy: (Math.random() - 0.5) * 0.3,
      text: SNIPPETS[Math.floor(Math.random() * SNIPPETS.length)],
      alpha: 0.08 + Math.random() * 0.1,
      size: 10 + Math.random() * 4,
      color: Math.random() > 0.7 ? '#dc2626' : '#3fb950'
    });
  }

  function frame() {
    ctx.clearRect(0, 0, W, H);
    ctx.font = FONT + 'px "JetBrains Mono",monospace';

    for (var i = 0; i < cols; i++) {
      var head = drops[i];
      var type = colType[i];

      for (var j = 0; j < TRAIL; j++) {
        var row = head - j;
        var y = row * FONT;
        if (y < 0 || y > H + FONT) continue;

        var alpha;
        var r, g, b;

        if (j === 0) {
          alpha = 0.85;
          r = 210; g = 255; b = 210;
          if (type === 'red')  { r = 255; g = 200; b = 200; }
          if (type === 'cyan') { r = 180; g = 255; b = 255; }
        } else {
          alpha = Math.pow((TRAIL - j) / TRAIL, 2.2) * 0.7;
          if (type === 'red')  { r = 220; g = 38;  b = 38;  }
          else if (type === 'cyan') { r = 0; g = 200; b = 200; }
          else { r = 0; g = 180; b = 60; }
        }

        ctx.fillStyle = 'rgba(' + r + ',' + g + ',' + b + ',' + alpha + ')';
        ctx.fillText(CHARS[Math.floor(Math.random() * CHARS.length)], i * FONT, y);
      }

      drops[i] += speeds[i];
      if (drops[i] * FONT > H + TRAIL * FONT && Math.random() > 0.975) {
        drops[i] = -Math.floor(Math.random() * 50);
      }
    }

    /* Floating particles */
    for (var k = 0; k < particles.length; k++) {
      var pt = particles[k];
      pt.x += pt.vx;
      pt.y += pt.vy;
      if (pt.x > W + 160) pt.x = -160;
      if (pt.x < -160)    pt.x = W + 160;
      if (pt.y > H + 50)  pt.y = -50;
      if (pt.y < -50)     pt.y = H + 50;

      ctx.save();
      ctx.globalAlpha = pt.alpha;
      ctx.font = pt.size + 'px "JetBrains Mono",monospace';
      ctx.fillStyle = pt.color;
      ctx.fillText(pt.text, pt.x, pt.y);
      ctx.restore();
    }

    requestAnimationFrame(frame);
  }

  resize();
  window.addEventListener('resize', resize);
  requestAnimationFrame(frame);
})();
