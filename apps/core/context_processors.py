import logging

from django.db import OperationalError, ProgrammingError
from .models import SiteSettings, MenuItem, SocialLink

logger = logging.getLogger(__name__)


def core_context(request):
    context = {
        'site_settings': None,
        'header_menu': [],
        'footer_menu': [],
        'social_links': [],
    }
    try:
        context['site_settings'] = SiteSettings.load()
        context['header_menu'] = MenuItem.objects.filter(is_active=True, menu_type="header").order_by("order")
        context['footer_menu'] = MenuItem.objects.filter(is_active=True, menu_type="footer").order_by("order")
        context['social_links'] = SocialLink.objects.filter(is_active=True).order_by("order")
    except (OperationalError, ProgrammingError):
        pass
    except Exception:
        logger.exception("Error loading core context data")
    return context
