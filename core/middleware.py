SESSION_KEY = 'sess_cal'

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local
_thread_locals = local()


class CalendarMiddleware(object):
    def _get_calendar_code(self, request):
        for attr in ('session', 'COOKIES'):
            if hasattr(request, attr):
                try:
                    return getattr(request, attr)[SESSION_KEY]
                except KeyError:
                    continue
        return 'ad'

    def process_request(self, request):
        if not SESSION_KEY in request.session or request.session[SESSION_KEY] is None:
            request.session[SESSION_KEY] = self._get_calendar_code(request)
        if not getattr(_thread_locals, SESSION_KEY, None):
            setattr(_thread_locals, SESSION_KEY, self._get_calendar_code(request))


def get_calendar():
    return getattr(_thread_locals, SESSION_KEY, None)
