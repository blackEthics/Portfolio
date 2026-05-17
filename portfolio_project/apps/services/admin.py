from django.contrib import admin
from .models import Service, ServiceTag


@admin.register(ServiceTag)
class ServiceTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    list_editable = ('color',)
    search_fields = ('name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'order')
    list_editable = ('order',)
    filter_horizontal = ('tags',)
