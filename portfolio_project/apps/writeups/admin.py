from django.contrib import admin
from .models import Writeup, WriteupTag


@admin.register(WriteupTag)
class WriteupTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    list_editable = ('color',)
    search_fields = ('name',)


@admin.register(Writeup)
class WriteupAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty_level', 'published_at', 'is_featured', 'read_time_display')
    list_editable = ('is_featured', 'difficulty_level')
    list_filter = ('is_featured', 'category', 'difficulty_level', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    search_fields = ('title', 'excerpt', 'content')
    date_hierarchy = 'published_at'
    readonly_fields = ('read_time_display',)
    fieldsets = (
        ('Identity', {'fields': ('title', 'slug', 'category', 'difficulty_level', 'is_featured')}),
        ('Content', {'fields': ('excerpt', 'content', 'thumbnail')}),
        ('Meta', {'fields': ('published_at', 'read_time_min', 'read_time_max', 'read_time_display', 'thumb_label')}),
        ('Tags', {'fields': ('tags',)}),
    )
