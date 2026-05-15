from django.shortcuts import render

from .models import Project
from .services import DUMMY_PROJECTS, LANGUAGE_COLORS, fetch_github_repos


def _db_projects_to_unified(db_projects):
    result = []
    for p in db_projects:
        result.append({
            'name': p.title,
            'description': p.excerpt,
            'language': 'Python',
            'language_color': LANGUAGE_COLORS['Python'],
            'stars': 0,
            'forks': 0,
            'topics': [t.name for t in p.tags.all()],
            'html_url': p.github_url or p.project_url or '#',
            'updated_at': p.created_at.strftime('%b %d, %Y'),
            'is_dummy': False,
        })
    return result


def list_view(request):
    github_repos = fetch_github_repos()
    db_projects = list(Project.objects.prefetch_related('tags').all())

    if github_repos:
        all_projects = github_repos
    elif db_projects:
        all_projects = _db_projects_to_unified(db_projects)
    else:
        all_projects = DUMMY_PROJECTS

    lang_filter = request.GET.get('lang', '').strip()
    search_query = request.GET.get('q', '').strip()

    all_languages = sorted({
        p['language'] for p in all_projects
        if p.get('language') and p['language'] != 'Unknown'
    })

    projects = all_projects
    if lang_filter:
        projects = [p for p in projects if p.get('language', '').lower() == lang_filter.lower()]
    if search_query:
        q = search_query.lower()
        projects = [
            p for p in projects
            if q in p['name'].lower() or q in p.get('description', '').lower()
        ]

    return render(request, 'projects/list.html', {
        'projects': projects,
        'all_languages': all_languages,
        'active_lang': lang_filter,
        'search_query': search_query,
        'total_count': len(all_projects),
    })
