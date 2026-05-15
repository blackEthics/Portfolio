from django.contrib import admin
from .models import SkillCategory, Skill


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 3
    fields = ('name', 'order')


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('label', 'order')
    list_editable = ('order',)
    inlines = [SkillInline]
