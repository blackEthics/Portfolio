from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Writeup, WriteupTag


def list_view(request):
    tag_slug = request.GET.get('tag', '').strip()
    active_category = request.GET.get('category', '').strip()
    search_q = request.GET.get('q', '').strip()

    writeups = Writeup.objects.prefetch_related('tags').all()
    active_tag = None

    if tag_slug:
        active_tag = WriteupTag.objects.filter(name__iexact=tag_slug).first()
        if active_tag:
            writeups = writeups.filter(tags=active_tag)

    if active_category:
        writeups = writeups.filter(category=active_category)

    if search_q:
        writeups = writeups.filter(
            Q(title__icontains=search_q) | Q(excerpt__icontains=search_q)
        )

    featured = (
        Writeup.objects.filter(is_featured=True).prefetch_related('tags')[:3]
        if not search_q and not active_tag and not active_category
        else []
    )

    return render(request, 'writeups/list.html', {
        'writeups': writeups,
        'all_tags': WriteupTag.objects.all(),
        'active_tag': active_tag,
        'featured': featured,
        'categories': Writeup.CATEGORY_CHOICES,
        'active_category': active_category,
        'search_q': search_q,
    })


def detail_view(request, slug):
    writeup = get_object_or_404(Writeup, slug=slug)

    all_writeups = list(Writeup.objects.order_by('-published_at').only('pk', 'slug', 'title'))
    idx = next((i for i, w in enumerate(all_writeups) if w.pk == writeup.pk), None)
    prev_writeup = all_writeups[idx + 1] if idx is not None and idx + 1 < len(all_writeups) else None
    next_writeup = all_writeups[idx - 1] if idx is not None and idx > 0 else None

    related = (
        Writeup.objects
        .exclude(pk=writeup.pk)
        .filter(tags__in=writeup.tags.all())
        .distinct()
        .prefetch_related('tags')[:3]
    )
    if not related.exists():
        related = Writeup.objects.exclude(pk=writeup.pk).prefetch_related('tags')[:3]

    return render(request, 'writeups/detail.html', {
        'writeup': writeup,
        'related': related,
        'prev_writeup': prev_writeup,
        'next_writeup': next_writeup,
    })
