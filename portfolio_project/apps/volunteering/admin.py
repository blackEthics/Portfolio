from django.contrib import admin
from .models import VolunteeringOrganization, VolunteeringRole


class VolunteeringRoleInline(admin.TabularInline):
    model = VolunteeringRole
    extra = 1
    fields = ('title', 'start_date', 'end_date', 'is_current', 'description', 'achievements', 'order')


@admin.register(VolunteeringOrganization)
class VolunteeringOrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'featured', 'location', 'total_duration', 'order')
    list_editable = ('category', 'featured', 'order')
    list_filter = ('category', 'featured')
    search_fields = ('name', 'location')
    inlines = [VolunteeringRoleInline]
