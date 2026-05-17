from django.core.cache import cache
from .models import SiteProfile

_CACHE_KEY = 'core_site_profile'
_CACHE_TTL = 300  # 5 minutes


def site_profile(request):
    profile = cache.get(_CACHE_KEY)
    if profile is None:
        profile = SiteProfile.objects.first()
        cache.set(_CACHE_KEY, profile, _CACHE_TTL)
    return {'site_profile': profile}
