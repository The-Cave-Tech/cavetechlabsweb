"""
Admin configuration for Cave Tech Labs website.
"""
from django.contrib import admin
from .models import Person, Project, Category, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'email', 'updated_at')
    
    fieldsets = (
        ('About Us', {
            'fields': ('about_title', 'about_content', 'image')
        }),
        ('Additional Content', {
            'fields': ('history',)
        }),
        ('Contact Information', {
            'fields': ('address', 'email', 'phone', 'instagram')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    def get_title(self, obj):
        """Display title in list."""
        return "Site Settings"
    get_title.short_description = "Setting"

    def has_add_permission(self, request):
        """Allow adding if no SiteSettings exists."""
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of SiteSettings."""
        return False

    def has_change_permission(self, request, obj=None):
        """Allow changing SiteSettings."""
        return True
    
    def changelist_view(self, request, extra_context=None):
        """Redirect to the edit page if there's only one instance."""
        response = super().changelist_view(request, extra_context)
        try:
            obj = SiteSettings.objects.first()
            if obj and request.GET.get('q') is None:
                # Automatically redirect to edit page
                from django.urls import reverse
                from django.shortcuts import redirect
                return redirect(reverse('admin:cavetechapp_sitesettings_change', args=[obj.pk]))
        except:
            pass
        return response


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'title', 'email', 'bio')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'title', 'email')
        }),
        ('Content', {
            'fields': ('bio', 'image')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'creator', 'featured', 'created_at')
    list_filter = ('category', 'featured', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'creator__name')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'creator')
        }),
        ('Content', {
            'fields': ('description', 'image')
        }),
        ('Display', {
            'fields': ('featured',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
