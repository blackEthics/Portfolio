from django.contrib import admin
from .models import Project, ProjectTag


@admin.register(ProjectTag)
class ProjectTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    list_editable = ('color',)
    search_fields = ('name',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_featured', 'order', 'created_at')
    list_editable = ('is_featured', 'order')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    search_fields = ('title', 'excerpt')
