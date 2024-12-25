from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Client, Project

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'created_at', 'created_by')  # Display these fields in the list view
    search_fields = ('client_name',)  # Add search functionality by client name
    list_filter = ('created_at',)  # Add filters by creation date
    readonly_fields = ('created_at', 'created_by') # Make these fields read-only in the admin form

    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'client', 'created_at', 'created_by')
    search_fields = ('project_name', 'client__client_name')
    list_filter = ('client', 'created_at') 
    filter_horizontal = ('users',) 
    readonly_fields = ('created_at', 'created_by')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)