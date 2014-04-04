try:
    import pytz
except ImportError:
    pass

try:
    import pygeoip
except ImportError:
    pass

try:
    import uwsgi
    running_uwsgi = True
except ImportError:
    running_uwsgi = False


from django.conf import settings
from django.utils import timezone


class XForwardedForMiddleware():
    def process_request(self, request):
        if request.META.has_key("HTTP_X_FORWARDED_FOR"):
            request.META["HTTP_X_PROXY_REMOTE_ADDR"] = request.META["REMOTE_ADDR"]
            parts = request.META["HTTP_X_FORWARDED_FOR"].split(",", 1)
            request.META["REMOTE_ADDR"] = parts[0]


db_loaded = False
db = None


def load_db():
    global db
    db = pygeoip.GeoIP(settings.GEOIP_DATABASE, pygeoip.MEMORY_CACHE)

    global db_loaded
    db_loaded = True


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


class TimezoneMiddleware(object):
    def process_request(self, request):
        if not db_loaded:
            load_db()

        tz = request.session.get('django_timezone')
        if not tz:
            ip = get_client_ip(request)
            # fetch the timezone from pygeoip
            if ip != '127.0.0.1':
                tz = db.time_zone_by_addr(ip)
                uwsgi.log(u"got timezone: %s, ip: %s" % (tz, ip))
            if not tz:
                timezone.get_default_timezone()
        if tz:
            timezone.activate(tz)
            request.session['django_timezone'] = tz
        else:
            timezone.deactivate()

