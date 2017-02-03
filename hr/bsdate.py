# This module uses njango module for Bikram Sambat Calendar
from django.utils.translation import ugettext
from njango.nepdate import bs, bs2ad
from datetime import date

month = {}
month[1] = ugettext('Baisakh')
month[2] = ugettext('Jestha')
month[3] = ugettext('Aasad')
month[4] = ugettext('Shrawan')
month[5] = ugettext('Bhadra')
month[6] = ugettext('Asoj')
month[7] = ugettext('Kartik')
month[8] = ugettext('Mansir')
month[9] = ugettext('Push')
month[10] = ugettext('Magh')
month[11] = ugettext('Falgun')
month[12] = ugettext('Chaitra')


def get_bs_datetime(ad_datetime, bs_date, format=None):
    time = ad_datetime.strftime('%X')
    if format=='AD':
        return ad_datetime.strftime('%d, %B, %Y'), time
    elif format=='BS':
        return bs_date.as_string(format='words'), time

    return str(bs_date), time



class BsDelta(object):
    def __init__(self, days):
        self.days = days

# TODO add time support to this module with tz info


class BSDate(object):

    def __init__(self, year, month, day):
        self._year = year
        self._month = month
        self._day = day

        try:
            bs[self._year]
        except KeyError:
            raise ValueError('No such year in njango nepdate calendar')
        if self._month > 12 or self._month < 1:
            raise ValueError('Incorrect Month')
        if self._day > bs[self._year][self._month - 1] or self._day < 1:
            raise ValueError('Incorrect date')

    def date_tuple(self):
        return (self._year, self._month, self._day)

    def as_string(self, format=None):
        if format == 'words':
            return '%s, %s, %s' % (
                str(self._day).zfill(2),
                month[self._month],
                str(self.year)
            )
        return '%s-%s-%s' % (
            str(self._year),
            str(self._month).zfill(2),
            str(self._day).zfill(2)
        )

    # Returns datetime.date type
    def as_ad(self):
        return date(*bs2ad(self.as_string()))

    @property
    def year(self):
        return self._year

    @property
    def month(self):
        return self._month

    @property
    def day(self):
        return self._day

    def __sub__(self, other):
        if type(self) == type(other):
            delta = date(*bs2ad(self.date_tuple())) - \
                date(*bs2ad(other.date_tuple()))
            return BsDelta(delta.days)
        else:
            raise TypeError('Cannot subtract %s with BSDate type' % (str(type(other))))

    def __eq__(self, other):
        if type(self) == type(other):
            if self.__sub__(other).days == 0:
                return True
            else:
                return False
        else:
            return False

    def __ne__(self, other):
        if type(self) == type(other):
            return not self.__eq__(other)
        else:
            return True

    def __lt__(self, other):
        if type(self) == type(other):
            if self.__sub__(other).days < 0:
                return True
            else:
                return False
        else:
            raise TypeError('Cannot compare %s with BSDate type' % (str(type(other))))

    def __le__(self, other):
        if type(self) == type(other):
            return self.__lt__(other) or self.__eq__(other)
        else:
            raise TypeError('Cannot compare %s with BSDate type' % (str(type(other))))

    def __gt__(self, other):
        if type(self) == type(other):
            if self.__sub__(other).days > 0:
                return True
            else:
                return False
        else:
            raise TypeError('Cannot compare %s with BSDate type' % (str(type(other))))

    def __ge__(self, other):
        if type(self) == type(other):
            return self.__gt__(other) or self.__eq__(other)
        raise TypeError('Cannot compare %s with BSDate type' % (str(type(other))))

    def __repr__(self):
        return  'BSDate - ' + self.as_string()

    def __str__(self):
        return self.as_string()
