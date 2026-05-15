from django.contrib import admin
from .models import ResearchPaper, ResearchTag


@admin.register(ResearchTag)
class ResearchTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    list_editable = ('color',)
    search_fields = ('name',)


@admin.register(ResearchPaper)
class ResearchPaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'venue', 'published_at', 'is_featured', 'order')
    list_editable = ('is_featured', 'order')
    list_filter = ('is_featured', 'published_at')
    search_fields = ('title', 'authors', 'venue', 'abstract')
    filter_horizontal = ('tags',)
    fieldsets = (
        (None, {
            'fields': ('title', 'authors', 'venue', 'published_at', 'publication_url', 'is_featured', 'order'),
        }),
        ('Content', {
            'fields': ('short_description', 'abstract'),
        }),
        ('Media & Tags', {
            'fields': ('certificate_image', 'tags'),
        }),
    )
