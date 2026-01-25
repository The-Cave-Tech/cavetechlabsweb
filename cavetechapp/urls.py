"""
URL routing for cavetechapp.
"""
from django.urls import path
from .views import (
    IndexView, AboutView, PeopleListView, PersonDetailView,
    ProjectsListView, ProjectDetailView
)

app_name = 'cavetechapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('people/', PeopleListView.as_view(), name='people_list'),
    path('people/<int:pk>/', PersonDetailView.as_view(), name='person_detail'),
    path('projects/', ProjectsListView.as_view(), name='projects_list'),
    path('projects/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
]
