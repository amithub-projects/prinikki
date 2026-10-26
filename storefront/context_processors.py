from .models import SiteSettings, Announcement, Category
from django.utils import timezone

def site_settings(request):
    settings_obj = SiteSettings.objects.first()
    now = timezone.now()
    live = Announcement.objects.filter(published=True, start_at__lte=now).filter(end_at__isnull=True) | Announcement.objects.filter(published=True, start_at__lte=now, end_at__gte=now)
    live = live.order_by('-priority', '-start_at')
    bar = [a for a in live if a.display_location in ('bar','both')]
    return {'site_settings': settings_obj, 'nav_categories': Category.objects.filter(active=True), 'bar_announcements': bar[:3]}
