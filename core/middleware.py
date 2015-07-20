SESSION_KEY = 'sess_cal'


def get_calendar_code(request):
    for attr in ('session', 'COOKIES'):
        if hasattr(request, attr):
            try:
                return getattr(request, attr)[SESSION_KEY]
            except KeyError:
                continue
    return 'ad'


class CalendarMiddleware(object):
    def process_request(self, request):
        if not hasattr(request, 'session'):
            return
        if not SESSION_KEY in request.session or request.session[SESSION_KEY] is None:
            request.session[SESSION_KEY] = get_calendar_code(False)
