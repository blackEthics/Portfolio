from django.contrib import admin
from .models import Experience, Achievement, ExperienceTag


@admin.register(ExperienceTag)
class ExperienceTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    list_editable = ('color',)
    search_fields = ('name',)


class AchievementInline(admin.TabularInline):
    model = Achievement
    extra = 1
    fields = ('text', 'order')


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'employment_type', 'is_current', 'order')
    list_editable = ('order', 'is_current')
    list_filter = ('employment_type', 'work_mode', 'is_current')
    search_fields = ('title', 'company')
    filter_horizontal = ('tags',)
    inlines = [AchievementInline]
