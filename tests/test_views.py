"""
View tests for The Cave Tech Labs application
"""
import pytest
from django.test import Client
from cavetechapp.models import Person, Project


class TestIndexView:
    """Test the homepage (index) view"""

    def test_index_returns_200(self, db, client):
        """Test that index view returns HTTP 200"""
        response = client.get('/')
        assert response.status_code == 200

    def test_index_uses_correct_template(self, db, client):
        """Test that index view uses correct template"""
        response = client.get('/')
        assert 'cavetechapp/index.html' in [t.name for t in response.templates]

    def test_index_shows_featured_projects(self, db, client, featured_project):
        """Test that featured projects appear on homepage"""
        response = client.get('/')
        assert featured_project in response.context['featured_projects']

    def test_index_shows_people(self, db, client, sample_person):
        """Test that people appear on homepage"""
        response = client.get('/')
        assert sample_person in response.context['people']

    def test_index_shows_only_featured_projects(self, db, client, featured_project, sample_project):
        """Test that only featured projects appear on homepage"""
        response = client.get('/')
        assert featured_project in response.context['featured_projects']
        assert sample_project not in response.context['featured_projects']

    def test_index_limits_featured_projects_to_6(self, db, client):
        """Test that homepage shows max 6 featured projects"""
        for i in range(10):
            Project.objects.create(
                title=f"Featured {i}",
                description="Test",
                category="software",
                featured=True
            )
        response = client.get('/')
        assert len(response.context['featured_projects']) == 6


class TestPeopleListView:
    """Test the people list view"""

    def test_people_list_returns_200(self, db, client):
        """Test that people list returns HTTP 200"""
        response = client.get('/people/')
        assert response.status_code == 200

    def test_people_list_uses_correct_template(self, db, client):
        """Test that people list uses correct template"""
        response = client.get('/people/')
        assert 'cavetechapp/people_list.html' in [t.name for t in response.templates]

    def test_people_list_shows_all_people(self, db, client):
        """Test that all people appear in list"""
        person1 = Person.objects.create(name="Person 1")
        person2 = Person.objects.create(name="Person 2")
        response = client.get('/people/')
        assert person1 in response.context['people']
        assert person2 in response.context['people']

    def test_people_list_empty_when_no_people(self, db, client):
        """Test that people list is empty when no people exist"""
        response = client.get('/people/')
        assert len(response.context['people']) == 0


class TestPersonDetailView:
    """Test the person detail view"""

    def test_person_detail_returns_200(self, db, client, sample_person):
        """Test that person detail returns HTTP 200"""
        response = client.get(f'/people/{sample_person.pk}/')
        assert response.status_code == 200

    def test_person_detail_uses_correct_template(self, db, client, sample_person):
        """Test that person detail uses correct template"""
        response = client.get(f'/people/{sample_person.pk}/')
        assert 'cavetechapp/person_detail.html' in [t.name for t in response.templates]

    def test_person_detail_shows_correct_person(self, db, client, sample_person):
        """Test that person detail shows the correct person"""
        response = client.get(f'/people/{sample_person.pk}/')
        assert response.context['person'] == sample_person

    def test_person_detail_shows_projects(self, db, client, sample_person, sample_project):
        """Test that person detail shows their projects"""
        response = client.get(f'/people/{sample_person.pk}/')
        assert sample_project in response.context['projects']

    def test_person_detail_404_for_nonexistent(self, db, client):
        """Test that person detail returns 404 for nonexistent person"""
        response = client.get('/people/9999/')
        assert response.status_code == 404


class TestProjectsListView:
    """Test the projects list view"""

    def test_projects_list_returns_200(self, db, client):
        """Test that projects list returns HTTP 200"""
        response = client.get('/projects/')
        assert response.status_code == 200

    def test_projects_list_uses_correct_template(self, db, client):
        """Test that projects list uses correct template"""
        response = client.get('/projects/')
        assert 'cavetechapp/projects_list.html' in [t.name for t in response.templates]

    def test_projects_list_shows_all_projects(self, db, client, sample_project):
        """Test that all projects appear in list"""
        response = client.get('/projects/')
        assert sample_project in response.context['projects']

    def test_projects_list_filter_by_category(self, db, client):
        """Test filtering projects by category"""
        Project.objects.create(
            title="Electronics Project",
            description="Test",
            category="electronics"
        )
        Project.objects.create(
            title="Software Project",
            description="Test",
            category="software"
        )
        response = client.get('/projects/?category=electronics')
        assert len(response.context['projects']) == 1
        assert response.context['projects'][0].category == "electronics"

    def test_projects_list_shows_available_categories(self, db, client):
        """Test that view shows available categories"""
        Project.objects.create(title="Project 1", description="Test", category="electronics")
        Project.objects.create(title="Project 2", description="Test", category="software")
        response = client.get('/projects/')
        assert "electronics" in response.context['categories']
        assert "software" in response.context['categories']

    def test_projects_list_category_filter_is_empty_string(self, db, client, sample_project):
        """Test that no category filter shows all projects"""
        response = client.get('/projects/?category=')
        assert sample_project in response.context['projects']


class TestProjectDetailView:
    """Test the project detail view"""

    def test_project_detail_returns_200(self, db, client, sample_project):
        """Test that project detail returns HTTP 200"""
        response = client.get(f'/projects/{sample_project.slug}/')
        assert response.status_code == 200

    def test_project_detail_uses_correct_template(self, db, client, sample_project):
        """Test that project detail uses correct template"""
        response = client.get(f'/projects/{sample_project.slug}/')
        assert 'cavetechapp/project_detail.html' in [t.name for t in response.templates]

    def test_project_detail_shows_correct_project(self, db, client, sample_project):
        """Test that project detail shows the correct project"""
        response = client.get(f'/projects/{sample_project.slug}/')
        assert response.context['project'] == sample_project

    def test_project_detail_shows_related_projects(self, db, client):
        """Test that project detail shows related projects in same category"""
        project1 = Project.objects.create(
            title="Electronics 1",
            description="Test",
            category="electronics"
        )
        project2 = Project.objects.create(
            title="Electronics 2",
            description="Test",
            category="electronics"
        )
        response = client.get(f'/projects/{project1.slug}/')
        assert project2 in response.context['related_projects']

    def test_project_detail_does_not_show_self_in_related(self, db, client, sample_project):
        """Test that project doesn't appear in its own related projects"""
        response = client.get(f'/projects/{sample_project.slug}/')
        assert sample_project not in response.context['related_projects']

    def test_project_detail_limits_related_to_3(self, db, client):
        """Test that project detail shows max 3 related projects"""
        project1 = Project.objects.create(
            title="Electronics 1",
            description="Test",
            category="electronics"
        )
        for i in range(5):
            Project.objects.create(
                title=f"Electronics {i+2}",
                description="Test",
                category="electronics"
            )
        response = client.get(f'/projects/{project1.slug}/')
        assert len(response.context['related_projects']) == 3

    def test_project_detail_404_for_nonexistent(self, db, client):
        """Test that project detail returns 404 for nonexistent project"""
        response = client.get('/projects/nonexistent-project/')
        assert response.status_code == 404
