from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('', include('apps.home.urls', namespace='home')),
    path('writeups/', include('apps.writeups.urls', namespace='writeups')),
    path('projects/', include('apps.projects.urls', namespace='projects')),
    path('research/', include('apps.research.urls', namespace='research')),
    path('volunteering/', include('apps.volunteering.urls', namespace='volunteering')),
]

# Custom error pages (active when DEBUG=False)
handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'

# Development-only media serving.
# In production, configure your web server (nginx/Apache) to serve MEDIA_ROOT
# at MEDIA_URL, or use a cloud storage backend (django-storages + S3/Cloudinary).
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
