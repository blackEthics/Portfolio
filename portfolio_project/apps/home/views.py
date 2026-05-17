import re
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.cache import cache

from apps.services.models import Service
from apps.skills.models import SkillCategory
from apps.certifications.models import Certification
from apps.experience.models import Experience
from apps.education.models import Education
from apps.writeups.models import Writeup
from apps.projects.models import Project
from apps.projects.services import DUMMY_PROJECTS, fetch_github_repos
from apps.core.models import ContactMessage
from apps.volunteering.models import VolunteeringOrganization, VolunteeringRole
from apps.research.models import ResearchPaper

_EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')


def _get_client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


def index(request):
    if request.method == 'POST':
        return _handle_contact(request)

    github_repos = fetch_github_repos()
    home_projects = (github_repos or DUMMY_PROJECTS)[:6]

    context = {
        'services': Service.objects.prefetch_related('tags').all(),
        'skill_categories': SkillCategory.objects.prefetch_related('skills').all(),
        'certifications': Certification.objects.all(),
        'experiences': Experience.objects.prefetch_related('achievements', 'tags').all(),
        'educations': Education.objects.prefetch_related('tags').all(),
        'featured_vol_orgs': VolunteeringOrganization.objects.filter(featured=True).prefetch_related('roles')[:3],
        'total_vol_orgs': VolunteeringOrganization.objects.count(),
        'total_vol_roles': VolunteeringRole.objects.count(),
        'research_papers': ResearchPaper.objects.prefetch_related('tags').all(),
        'featured_writeups': Writeup.objects.filter(is_featured=True).prefetch_related('tags')[:3],
        'all_writeups': Writeup.objects.prefetch_related('tags').all()[:5],
        'projects': Project.objects.filter(is_featured=True).prefetch_related('tags')[:6],
        'home_projects': home_projects,
        'form_success': request.session.pop('contact_success', False),
        'form_errors': request.session.pop('contact_errors', []),
    }
    return render(request, 'home/index.html', context)


def _handle_contact(request):
    contact_url = reverse('home:index') + '#contact'

    # Rate limiting: max 3 submissions per 10 minutes per IP
    ip = _get_client_ip(request)
    rate_key = f'contact_rate_{ip}'
    submissions = cache.get(rate_key, 0)
    if submissions >= 3:
        request.session['contact_errors'] = [
            'Too many submissions. Please wait a few minutes before trying again.'
        ]
        return HttpResponseRedirect(contact_url)
    cache.set(rate_key, submissions + 1, 600)

    first_name = request.POST.get('first_name', '').strip()
    last_name = request.POST.get('last_name', '').strip()
    email = request.POST.get('email', '').strip()
    subject = request.POST.get('subject', '').strip()
    message = request.POST.get('message', '').strip()

    errors = []
    if not first_name or len(first_name) > 50:
        errors.append('First name is required and must be under 50 characters.')
    if not last_name or len(last_name) > 50:
        errors.append('Last name is required and must be under 50 characters.')
    if not email or not _EMAIL_RE.match(email) or len(email) > 254:
        errors.append('A valid email address is required.')
    if not subject or len(subject) > 200:
        errors.append('Subject is required and must be under 200 characters.')
    if not message or len(message) > 5000:
        errors.append('Message is required and must be under 5,000 characters.')

    if errors:
        request.session['contact_errors'] = errors
        return HttpResponseRedirect(contact_url)

    ContactMessage.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        subject=subject,
        message=message,
    )
    request.session['contact_success'] = True
    return HttpResponseRedirect(contact_url)
