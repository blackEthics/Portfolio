from django.contrib import admin
from .models import Education, EducationTag


@admin.register(EducationTag)
class EducationTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    list_editable = ('color',)
    search_fields = ('name',)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'school', 'location', 'start_year', 'end_year', 'order')
    list_editable = ('order',)
    search_fields = ('degree', 'school')
    filter_horizontal = ('tags',)
