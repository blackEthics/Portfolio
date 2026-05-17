from django.shortcuts import render
from .models import VolunteeringOrganization, VolunteeringRole


def list_view(request):
    active_category = request.GET.get('category', '')
    orgs = VolunteeringOrganization.objects.prefetch_related('roles').all()
    if active_category:
        orgs = orgs.filter(category=active_category)

    context = {
        'orgs': orgs,
        'active_category': active_category,
        'categories': VolunteeringOrganization.CATEGORY_CHOICES,
        'total_orgs': VolunteeringOrganization.objects.count(),
        'total_roles': VolunteeringRole.objects.count(),
    }
    return render(request, 'volunteering/list.html', context)
