"""
Context processors for the cavetechapp.
"""
from .models import SiteSettings


def site_settings(request):
    """Make SiteSettings available to all templates."""
    try:
        settings = SiteSettings.get_settings()
    except:
        settings = None
    
    return {'settings': settings}
