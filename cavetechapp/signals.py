"""
Signals for the cavetechapp.
"""
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import SiteSettings


@receiver(post_migrate)
def create_site_settings(sender, **kwargs):
    """Create SiteSettings instance after migrations."""
    if sender.name == 'cavetechapp':
        SiteSettings.objects.get_or_create(pk=1, defaults={
            'about_title': 'About CaveTech',
            'about_content': 'Welcome to CaveTech - Oslo\'s premier maker space.',
            'history': '',
            'address': 'Oslo, Norway',
            'email': 'contact@cavetechlabs.com',
            'instagram': '',
            'phone': '',
        })
