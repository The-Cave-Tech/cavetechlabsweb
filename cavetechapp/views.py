"""
Views for the Cave Tech Labs website.
"""
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Person, Project, Category, SiteSettings


class IndexView(View):
    """Home page view."""

    def get(self, request):
        featured_projects = Project.objects.filter(featured=True)[:6]
        people = Person.objects.all()
        context = {
            'featured_projects': featured_projects,
            'people': people,
        }
        return render(request, 'cavetechapp/index.html', context)


class AboutView(View):
    """About Us page view."""

    def get(self, request):
        settings = SiteSettings.get_settings()
        context = {'settings': settings}
        return render(request, 'cavetechapp/about.html', context)


class PeopleListView(View):
    """View listing all members."""

    def get(self, request):
        people = Person.objects.all()
        context = {'people': people}
        return render(request, 'cavetechapp/people_list.html', context)


class PersonDetailView(View):
    """View for individual person profile."""

    def get(self, request, pk):
        person = get_object_or_404(Person, pk=pk)
        projects = person.projects.all()
        context = {'person': person, 'projects': projects}
        return render(request, 'cavetechapp/person_detail.html', context)


class ProjectsListView(View):
    """View listing all projects with filtering."""

    def get(self, request):
        projects = Project.objects.all()
        category_slug = request.GET.get('category')
        if category_slug:
            projects = projects.filter(category__slug=category_slug)
        categories = Category.objects.all()
        context = {
            'projects': projects,
            'categories': categories,
            'selected_category': category_slug,
        }
        return render(request, 'cavetechapp/projects_list.html', context)


class ProjectDetailView(View):
    """View for individual project details."""

    def get(self, request, slug):
        project = get_object_or_404(Project, slug=slug)
        related_projects = Project.objects.filter(category=project.category).exclude(pk=project.pk)[:3]
        context = {
            'project': project,
            'related_projects': related_projects,
        }
        return render(request, 'cavetechapp/project_detail.html', context)
