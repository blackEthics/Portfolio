from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.home.urls', namespace='home')),
    path('writeups/', include('apps.writeups.urls', namespace='writeups')),
    path('projects/', include('apps.projects.urls', namespace='projects')),
    path('research/', include('apps.research.urls', namespace='research')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
