from django.contrib import admin
from .models import Certification


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'issuer', 'category', 'issue_date', 'status', 'order')
    list_editable = ('order', 'status')
    list_filter = ('status', 'issuer')
    search_fields = ('name', 'issuer', 'category')
    fieldsets = (
        (None, {
            'fields': ('name', 'short_name', 'category', 'issuer',
                       'issue_date', 'status', 'credential_url', 'order')
        }),
        ('Content', {
            'fields': ('description', 'cert_image')
        }),
    )
