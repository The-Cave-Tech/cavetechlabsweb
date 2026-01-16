"""
Model tests for The Cave Tech Labs application
"""
import pytest
from django.test import TestCase
from cavetechapp.models import Person, Project


class TestPersonModel:
    """Test the Person model"""

    def test_person_creation(self, db):
        """Test that a person can be created"""
        person = Person.objects.create(
            name="John Doe",
            title="Founder",
            email="john@example.com"
        )
        assert person.name == "John Doe"
        assert person.title == "Founder"
        assert person.email == "john@example.com"

    def test_person_string_representation(self, db):
        """Test that str(person) returns the name"""
        person = Person.objects.create(name="Alice Smith")
        assert str(person) == "Alice Smith"

    def test_person_ordering(self, db):
        """Test that people are ordered by name alphabetically"""
        person1 = Person.objects.create(name="Zoe Brown")
        person2 = Person.objects.create(name="Alice Smith")
        people = list(Person.objects.all())
        assert people[0].name == "Alice Smith"
        assert people[1].name == "Zoe Brown"

    def test_person_optional_fields(self, db):
        """Test that optional fields can be empty"""
        person = Person.objects.create(name="Minimal Person")
        assert person.title == ""
        assert person.bio == ""
        assert person.email == ""
        assert not person.image  # Image field is empty

    def test_person_with_all_fields(self, db):
        """Test person with all fields populated"""
        person = Person.objects.create(
            name="Complete Person",
            title="Instructor",
            bio="A complete bio",
            email="complete@example.com"
        )
        assert person.name == "Complete Person"
        assert person.bio == "A complete bio"

    def test_person_has_projects_relationship(self, db, sample_person, sample_project):
        """Test that person can have multiple projects"""
        assert sample_person.projects.count() == 1
        assert sample_person.projects.first() == sample_project


class TestProjectModel:
    """Test the Project model"""

    def test_project_creation(self, db, sample_person):
        """Test that a project can be created"""
        project = Project.objects.create(
            title="Cool Project",
            description="A cool project",
            category="electronics",
            creator=sample_person
        )
        assert project.title == "Cool Project"
        assert project.category == "electronics"
        assert project.creator == sample_person

    def test_project_string_representation(self, db, sample_project):
        """Test that str(project) returns the title"""
        assert str(sample_project) == "Test Project"

    def test_project_slug_auto_generation(self, db):
        """Test that slug is auto-generated from title"""
        project = Project.objects.create(
            title="My Awesome Project",
            description="Test",
            category="software"
        )
        assert project.slug == "my-awesome-project"

    def test_project_slug_uniqueness(self, db):
        """Test that slug must be unique"""
        Project.objects.create(
            title="Unique Project",
            description="Test",
            category="software"
        )
        with pytest.raises(Exception):  # IntegrityError
            Project.objects.create(
                title="Unique Project",
                description="Test",
                category="software"
            )

    def test_project_featured_flag(self, db, featured_project):
        """Test that featured flag works"""
        assert featured_project.featured is True
        not_featured = Project.objects.create(
            title="Not Featured",
            description="Test",
            category="software"
        )
        assert not_featured.featured is False

    def test_project_ordering(self, db):
        """Test that projects are ordered by created_at (newest first)"""
        project1 = Project.objects.create(
            title="First",
            description="Test",
            category="software"
        )
        project2 = Project.objects.create(
            title="Second",
            description="Test",
            category="software"
        )
        projects = list(Project.objects.all())
        assert projects[0].title == "Second"
        assert projects[1].title == "First"

    def test_project_creator_optional(self, db):
        """Test that project can exist without creator"""
        project = Project.objects.create(
            title="No Creator",
            description="Test",
            category="software"
        )
        assert project.creator is None

    def test_project_categories(self, db):
        """Test all project categories"""
        categories = [
            '3d_printing',
            'woodworking',
            'metalworking',
            'electronics',
            'software',
            'art',
            'robotics',
            'other'
        ]
        for i, category in enumerate(categories):
            project = Project.objects.create(
                title=f"Project {i}",
                description="Test",
                category=category
            )
            assert project.category == category

    def test_project_creator_deletion_behavior(self, db, sample_person, sample_project):
        """Test that deleting person sets project creator to null"""
        assert sample_project.creator == sample_person
        sample_person.delete()
        sample_project.refresh_from_db()
        assert sample_project.creator is None
