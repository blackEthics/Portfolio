from django.contrib import admin
from .models import Education, EducationTag


@admin.register(EducationTag)
class EducationTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'school', 'start_year', 'end_year', 'grade', 'order')
    list_editable = ('order',)
    search_fields = ('degree', 'school')
    filter_horizontal = ('tags',)
