from django.shortcuts import render, redirect
from django.contrib import messages

from apps.services.models import Service
from apps.skills.models import SkillCategory
from apps.certifications.models import Certification
from apps.experience.models import Experience
from apps.education.models import Education
from apps.writeups.models import Writeup
from apps.projects.models import Project
from apps.projects.services import DUMMY_PROJECTS, fetch_github_repos
from apps.core.models import ContactMessage
from apps.volunteering.models import VolunteeringOrganization
from apps.research.models import ResearchPaper


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
        'volunteering_orgs': VolunteeringOrganization.objects.prefetch_related('roles').all(),
        'research_papers': ResearchPaper.objects.prefetch_related('tags').all(),
        'featured_writeups': Writeup.objects.filter(is_featured=True).prefetch_related('tags')[:3],
        'all_writeups': Writeup.objects.prefetch_related('tags').all()[:5],
        'projects': Project.objects.filter(is_featured=True).prefetch_related('tags')[:6],
        'home_projects': home_projects,
        'form_success': request.session.pop('contact_success', False),
    }
    return render(request, 'home/index.html', context)


def _handle_contact(request):
    ContactMessage.objects.create(
        first_name=request.POST.get('first_name', '').strip(),
        last_name=request.POST.get('last_name', '').strip(),
        email=request.POST.get('email', '').strip(),
        subject=request.POST.get('subject', '').strip(),
        message=request.POST.get('message', '').strip(),
    )
    request.session['contact_success'] = True
    return redirect('home:index', permanent=False)
