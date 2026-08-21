import logging
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

def send_lead_notification(lead):
    recipients = []
    if getattr(settings, "LEAD_NOTIFY_EMAIL", ""):
        recipients.append(settings.LEAD_NOTIFY_EMAIL)
    if not recipients:
        try:
            from apps.core.models import SiteSettings
            ss = SiteSettings.load()
            if ss.email:
                recipients.append(ss.email)
        except Exception:
            logger.exception("site settings email unavailable")
    if not recipients:
        return False
    subject = "لید جدید: " + lead.full_name
    message = (
        "نام: " + lead.full_name + "\n"
        "تلفن: " + lead.phone + "\n"
        "ایمیل: " + (lead.email or "-") + "\n"
        "خدمت: " + lead.get_service_type_display() + "\n"
        "بودجه: " + lead.get_budget_display() + "\n"
        "پیام: " + (lead.message or "-") + "\n"
        "منبع: " + (lead.source_page or "-") + "\n"
    )
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients, fail_silently=False)
        return True
    except Exception:
        logger.exception("lead notification failed")
        return False