/* ── animations.js ── Intersection observer fade-ins + live terminal ── */

document.addEventListener('DOMContentLoaded', function () {

  // ── Fade-in observer ──
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.fade-in').forEach(function (el) {
    observer.observe(el);
  });

  // ── Live terminal ──
  var termBody = document.getElementById('term-body');
  if (!termBody) return;

  var termCmds = [
    '$ nmap -sV target.com',
    'Starting Nmap...',
    '80/tcp  open  http',
    '443/tcp open  https',
    '22/tcp  open  ssh',
    '$ python3 exploit.py',
    '[*] Connecting...',
    '[+] Shell obtained!',
    '$ msfconsole -q',
    'use exploit/multi/handler',
    'set LHOST 10.0.0.1',
    'exploit',
    '[*] Meterpreter session 1',
    '$ gobuster dir -u target.com',
    'Found: /admin [200]',
    'Found: /login [200]',
    'Found: /backup [403]',
    '$ nikto -h target.com',
    '+ XSS filter not set',
    '$ sqlmap -u target.com/id=1',
    '[*] testing...',
    '[+] Parameter vulnerable!',
    '$ hydra -l admin -P rockyou.txt',
    '[22][ssh] login: admin',
    '$ whoami',
    'root'
  ];

  var termIdx = 0;

  function appendLine() {
    var line = document.createElement('div');
    var cmd = termCmds[termIdx % termCmds.length];
    line.textContent = cmd;
    if (cmd.startsWith('$')) {
      line.style.color = '#f0f6fc';
      line.style.fontWeight = '500';
    } else if (cmd.startsWith('[+]')) {
      line.style.color = '#3fb950';
    } else if (cmd.startsWith('[*]')) {
      line.style.color = '#58a6ff';
    } else if (cmd.startsWith('Found:')) {
      line.style.color = '#ffa657';
    }
    termBody.appendChild(line);
    termBody.scrollTop = termBody.scrollHeight;
    termIdx++;
    if (termBody.children.length > 60) {
      termBody.removeChild(termBody.firstChild);
    }
  }

  appendLine();
  setInterval(appendLine, 1500);

});
