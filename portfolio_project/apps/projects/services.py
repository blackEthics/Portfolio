from datetime import datetime

from django.conf import settings
from django.core.cache import cache

try:
    import requests as _requests
    _REQUESTS_AVAILABLE = True
except ImportError:
    _REQUESTS_AVAILABLE = False

LANGUAGE_COLORS = {
    'Python': '#3572A5',
    'JavaScript': '#f1e05a',
    'TypeScript': '#2b7489',
    'Go': '#00ADD8',
    'Rust': '#dea584',
    'C': '#555555',
    'C++': '#f34b7d',
    'Shell': '#89e051',
    'Bash': '#89e051',
    'HTML': '#e34c26',
    'CSS': '#563d7c',
    'Java': '#b07219',
    'PHP': '#4F5D95',
    'Ruby': '#701516',
    'PowerShell': '#012456',
    'Dockerfile': '#384d54',
    'Makefile': '#427819',
    'Lua': '#000080',
    'Perl': '#0298c3',
    'Swift': '#F05138',
    'Kotlin': '#A97BFF',
    'Scala': '#c22d40',
    'R': '#198CE7',
    'YAML': '#cb171e',
}

DUMMY_PROJECTS = [
    {
        'name': 'CyberPulse-Scanner',
        'description': 'Advanced network security scanner with real-time vulnerability detection and CVE correlation. Automates reconnaissance and fingerprinting of target systems with comprehensive reporting.',
        'language': 'Python',
        'language_color': '#3572A5',
        'stars': 128,
        'forks': 34,
        'topics': ['security', 'scanner', 'pentest', 'nmap'],
        'html_url': '#',
        'updated_at': 'Apr 15, 2026',
        'is_dummy': True,
    },
    {
        'name': 'VulnHunter-Framework',
        'description': 'Automated vulnerability assessment framework for web applications. Detects OWASP Top 10 vulnerabilities including SQLi, XSS, CSRF, and SSRF with detailed exploit chains.',
        'language': 'Python',
        'language_color': '#3572A5',
        'stars': 87,
        'forks': 21,
        'topics': ['owasp', 'web-security', 'bug-bounty', 'ctf'],
        'html_url': '#',
        'updated_at': 'Mar 22, 2026',
        'is_dummy': True,
    },
    {
        'name': 'CryptoShield',
        'description': 'Cryptographic analysis toolkit for identifying weak encryption implementations, broken cipher modes, and insecure key management patterns in modern applications.',
        'language': 'Python',
        'language_color': '#3572A5',
        'stars': 63,
        'forks': 15,
        'topics': ['cryptography', 'security', 'analysis', 'cipher'],
        'html_url': '#',
        'updated_at': 'Feb 10, 2026',
        'is_dummy': True,
    },
    {
        'name': 'PhishGuard-ML',
        'description': 'Machine learning-powered phishing detection system using NLP and URL analysis. Classifies phishing attempts with 98.3% accuracy across email and web attack vectors.',
        'language': 'Python',
        'language_color': '#3572A5',
        'stars': 156,
        'forks': 42,
        'topics': ['machine-learning', 'phishing', 'nlp', 'security'],
        'html_url': '#',
        'updated_at': 'Apr 01, 2026',
        'is_dummy': True,
    },
    {
        'name': 'NetSentinel',
        'description': 'Real-time network intrusion detection system with behavioral analysis and anomaly detection. Monitors traffic patterns and generates alerts for suspicious lateral movement.',
        'language': 'Go',
        'language_color': '#00ADD8',
        'stars': 74,
        'forks': 18,
        'topics': ['ids', 'network-security', 'real-time', 'go'],
        'html_url': '#',
        'updated_at': 'Mar 05, 2026',
        'is_dummy': True,
    },
    {
        'name': 'PayloadForge',
        'description': 'Custom payload generator for authorized penetration testing engagements. Supports obfuscation, encoding, and AV-evasion techniques for various target environments.',
        'language': 'Python',
        'language_color': '#3572A5',
        'stars': 203,
        'forks': 67,
        'topics': ['payload', 'red-team', 'obfuscation', 'pentest'],
        'html_url': '#',
        'updated_at': 'Apr 20, 2026',
        'is_dummy': True,
    },
]


def _fmt_date(iso_str):
    """Convert '2026-04-15T12:00:00Z' to 'Apr 15, 2026'."""
    try:
        return datetime.strptime(iso_str[:10], '%Y-%m-%d').strftime('%b %d, %Y')
    except Exception:
        return iso_str[:10]


def fetch_github_repos(username=None, token=None):
    """
    Fetch public, non-fork repos for *username* from the GitHub REST API.
    Returns a list of unified project dicts, or None on failure.
    Results are cached for GITHUB_CACHE_SECONDS (default 300 s).
    """
    username = username or getattr(settings, 'GITHUB_USERNAME', '')
    token = token or getattr(settings, 'GITHUB_TOKEN', '')

    if not username or not _REQUESTS_AVAILABLE:
        return None

    cache_key = f'github_repos_{username}'
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    headers = {'Accept': 'application/vnd.github.v3+json'}
    if token:
        headers['Authorization'] = f'token {token}'

    try:
        resp = _requests.get(
            f'https://api.github.com/users/{username}/repos',
            params={'sort': 'updated', 'per_page': 100, 'type': 'owner'},
            headers=headers,
            timeout=6,
        )
        if resp.status_code != 200:
            return None

        result = []
        for repo in resp.json():
            if repo.get('fork') or repo.get('private'):
                continue
            lang = repo.get('language') or 'Unknown'
            result.append({
                'name': repo['name'],
                'description': repo.get('description') or '',
                'language': lang,
                'language_color': LANGUAGE_COLORS.get(lang, '#8b949e'),
                'stars': repo.get('stargazers_count', 0),
                'forks': repo.get('forks_count', 0),
                'topics': repo.get('topics', []),
                'html_url': repo.get('html_url', '#'),
                'updated_at': _fmt_date(repo.get('updated_at', '')),
                'is_dummy': False,
            })

        result.sort(key=lambda x: x['stars'], reverse=True)

        cache_secs = getattr(settings, 'GITHUB_CACHE_SECONDS', 300)
        cache.set(cache_key, result, cache_secs)
        return result

    except Exception:
        return None
