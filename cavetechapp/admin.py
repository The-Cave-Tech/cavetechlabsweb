"""
Admin configuration for Cave Tech Labs website.
"""
from django.contrib import admin
from .models import Person, Project, Category, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('email', 'updated_at')
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

    def has_add_permission(self, request):
        """Prevent adding more than one SiteSettings instance."""
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of SiteSettings."""
        return False


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
