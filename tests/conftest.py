"""
Pytest configuration and shared fixtures
"""
import pytest
import os
import django
from django.conf import settings

# Ensure Django settings are configured for tests
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cavetechlabs.settings')
if not settings.configured:
    django.setup()


@pytest.fixture
def sample_person(db):
    """Fixture: Create a sample person"""
    from cavetechapp.models import Person
    return Person.objects.create(
        name="Test Person",
        title="Test Role",
        email="test@example.com",
        bio="Test bio"
    )


@pytest.fixture
def sample_project(db, sample_person):
    """Fixture: Create a sample project"""
    from cavetechapp.models import Project
    return Project.objects.create(
        title="Test Project",
        description="This is a test project",
        category="electronics",
        creator=sample_person,
        featured=False
    )


@pytest.fixture
def featured_project(db, sample_person):
    """Fixture: Create a featured project"""
    from cavetechapp.models import Project
    return Project.objects.create(
        title="Featured Project",
        description="This is a featured project",
        category="3d_printing",
        creator=sample_person,
        featured=True
    )
