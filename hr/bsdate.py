# This module uses njango module for Bikram Sambat Calendar
from njango.nepdate import bs, bs2ad
from datetime import date


class BsDelta(object):

    def __init__(self, days):
        self.days = days


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

    def as_string(self):
        return '%d-%d-%d' % (
            self._year,
            self._month,
            self._day
        )

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
        delta = date(*bs2ad(self.date_tuple())) - \
            date(*bs2ad(other.date_tuple()))
        return BsDelta(delta.days)

    def __eq__(self, other):
        if self.__sub__(other).days == 0:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if self.__sub__(other).days < 0:
            return True
        else:
            return False

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        if self.__sub__(other).days > 0:
            return True
        else:
            return False

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)
