"""
Admin configuration for Cave Tech Labs website.
"""
from django.contrib import admin
from .models import Person, Project


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
