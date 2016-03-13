import math
from functools import reduce
import math
import codecs


class Coder(object):
    ALPHABET = "bcdfghjklmnpqrstvwxyz0123456789BCDFGHJKLMNPQRSTVWXYZ"
    BASE = len(ALPHABET)
    MAX_LEN = 6

    @staticmethod
    def rot13(s):
        enc = codecs.getencoder("rot-13")
        return enc(s)[0]

    @staticmethod
    def checksum(st):
        return reduce(lambda x, y: x + y, map(ord, st))

    @staticmethod
    def checksum_str(st):
        return str(reduce(lambda x, y: x + y, map(ord, st)))

    @staticmethod
    def check_checksum(st, chk_sum):
        return reduce(lambda x, y: x + y, map(ord, st)) == chk_sum

    @staticmethod
    def encode_id(n):
        pad = Coder.MAX_LEN - 1
        n = int(n + pow(Coder.BASE, pad))
        s = []
        t = int(math.log(n, Coder.BASE))
        while True:
            bcp = int(pow(Coder.BASE, t))
            a = int(n / bcp) % Coder.BASE
            s.append(Coder.ALPHABET[a:a + 1])
            n -= a * bcp
            t -= 1
            if t < 0: break
        return "".join(reversed(s))

    @staticmethod
    def decode_id(n):
        n = "".join(reversed(n))
        s = 0
        l = len(n) - 1
        t = 0
        while True:
            bow = int(pow(Coder.BASE, l - t))
            s += Coder.ALPHABET.index(n[t:t + 1]) * bow
            t += 1
            if t > l: break
        pad = Coder.MAX_LEN - 1
        s = int(s - pow(Coder.BASE, pad))
        return int(s)

    @staticmethod
    def encode_date(date):
        return Coder.encode_id(int(date.strftime('%Y%m%d')))

    @staticmethod
    def decode_date(date):
        from datetime import datetime

        decoded = Coder.decode_id(date)
        return datetime.strptime(str(decoded), '%Y%m%d').date()
