"""
Admin tests for The Cave Tech Labs application
"""
import pytest
from django.contrib.admin.sites import AdminSite
from cavetechapp.admin import PersonAdmin, ProjectAdmin
from cavetechapp.models import Person, Project


class TestPersonAdmin:
    """Test Person admin configuration"""

    def test_person_admin_list_display(self):
        """Test that person admin displays correct fields"""
        assert 'name' in PersonAdmin.list_display
        assert 'title' in PersonAdmin.list_display
        assert 'email' in PersonAdmin.list_display

    def test_person_admin_list_filter(self):
        """Test that person admin has filters"""
        assert 'created_at' in PersonAdmin.list_filter

    def test_person_admin_search_fields(self):
        """Test that person admin has search"""
        assert 'name' in PersonAdmin.search_fields


class TestProjectAdmin:
    """Test Project admin configuration"""

    def test_project_admin_list_display(self):
        """Test that project admin displays correct fields"""
        assert 'title' in ProjectAdmin.list_display
        assert 'category' in ProjectAdmin.list_display
        assert 'creator' in ProjectAdmin.list_display

    def test_project_admin_list_filter(self):
        """Test that project admin has filters"""
        assert 'category' in ProjectAdmin.list_filter
        assert 'featured' in ProjectAdmin.list_filter

    def test_project_admin_search_fields(self):
        """Test that project admin has search"""
        assert 'title' in ProjectAdmin.search_fields

    def test_project_admin_prepopulated_fields(self):
        """Test that slug is auto-populated from title"""
        assert 'slug' in ProjectAdmin.prepopulated_fields
        assert ProjectAdmin.prepopulated_fields['slug'] == ('title',)
