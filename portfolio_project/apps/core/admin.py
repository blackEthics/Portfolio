from django.contrib import admin
from .models import SiteProfile, ContactMessage


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identity', {
            'fields': ('name', 'hero_label', 'title_roles', 'bio',
                       'profile_photo', 'profile_initials')
        }),
        ('Social Links', {
            'fields': ('github_url', 'linkedin_url', 'tryhackme_url')
        }),
        ('Contact Info', {
            'fields': ('email', 'phone', 'location', 'response_note')
        }),
        ('Footer', {
            'fields': ('footer_tagline', 'footer_location')
        }),
    )

    def has_add_permission(self, request):
        return not SiteProfile.objects.exists()


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'subject')
    readonly_fields = ('first_name', 'last_name', 'email', 'subject', 'message', 'created_at')
    list_editable = ('is_read',)
    ordering = ('-created_at',)
