from datetime import date
from django.template import Library
from njango.nepdate import bs2ad
from project.models import NPRExchange

register = Library()


@register.filter
def against(jv, acc):
    if jv.dr == acc:
        return jv.cr
    if jv.cr == acc:
        return jv.dr


@register.filter
def is_dr(jv, acc):
    return jv.dr == acc


@register.filter
def Ymd(dt):
    if type(dt) == date:
        return str(dt)
    else:
        return str(date(*bs2ad(dt)))


@register.filter
def get_exchange(dt):
    if type(dt) == date:
        return NPRExchange.get(dt)
    else:
        return NPRExchange.get(date(*bs2ad(dt)))
