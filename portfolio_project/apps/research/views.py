from django.db.models import Q
from django.shortcuts import render
from .models import ResearchPaper, ResearchTag


def list_view(request):
    search_q = request.GET.get('q', '').strip()
    active_tag_name = request.GET.get('tag', '').strip()

    papers = ResearchPaper.objects.prefetch_related('tags').all()

    active_tag = None
    if active_tag_name:
        try:
            active_tag = ResearchTag.objects.get(name=active_tag_name)
            papers = papers.filter(tags=active_tag)
        except ResearchTag.DoesNotExist:
            pass

    if search_q:
        papers = papers.filter(
            Q(title__icontains=search_q) |
            Q(authors__icontains=search_q) |
            Q(abstract__icontains=search_q) |
            Q(venue__icontains=search_q)
        ).distinct()

    highlighted = papers.filter(is_featured=True) if not search_q and not active_tag else None

    all_tags = ResearchTag.objects.filter(papers__isnull=False).distinct().order_by('name')

    context = {
        'papers': papers,
        'highlighted': highlighted,
        'all_tags': all_tags,
        'active_tag': active_tag,
        'search_q': search_q,
        'total_count': ResearchPaper.objects.count(),
    }
    return render(request, 'research/list.html', context)
