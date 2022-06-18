"""Useful Functions with Built-in Library"""

import os
import sys
import html
import time
import threading
import traceback
import urllib.parse
import urllib.request

# LOG = time.strftime('RECORD_%Y%m%d_%H%M%S.log')
LOG = time.strftime('LOG_%Y%m%d_%H%M%S.txt')


__all__ = list(globals())


# ---------------------------------------------------------------------------
# Debug
# ---------------------------------------------------------------------------


def tag():
    return time.strftime('[%Y-%m-%d %H:%M:%S] ')


def log(*value):
    s = tag() + ' '.join(map(str, value))
    with open(LOG, 'a', encoding='u8') as f:
        f.write(s)


def check(obj, rule=bool):  # rule=lambda s: s.startswith('Get')
    print('\nobj:', obj)
    for key in filter(rule, dir(obj)):
        attr = getattr(obj, key)
        print('\nkey:', key)
        if not callable(attr):
            print('value:', attr)
        else:
            try:
                print('value call:', attr())
            except TypeError as e:
                print('value callable:', attr, 'TypeError:', e)


# ---------------------------------------------------------------------------
# File system
# ---------------------------------------------------------------------------


def safe_name(filename, repl=' '):  # not include path
    for c in '\r\n\t\\/:*?"<>|':
        if repl is None:
            filename = filename.replace(c, urllib.parse.quote(c, ''))
        else:
            filename = filename.replace(c, repl)
    return filename


def unique(p, dash='-'):
    root, ext = os.path.splitext(p)
    n = 0
    while os.path.exists(p):
        n += 1
        p = '%s%s%d%s' % (root, dash, n, ext)
    return p


# ---------------------------------------------------------------------------
# Web
# ---------------------------------------------------------------------------


escape = html.escape
unescape = html.unescape
quote = urllib.parse.quote_plus  # quote every word include '/'
unquote = urllib.parse.unquote


def urlopen(url, timeout=5):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request, timeout=timeout)
    return response.read()


# ---------------------------------------------------------------------------
# ...
# ---------------------------------------------------------------------------


def findpair(s, p1='(', p2=')', st=0):
    n1 = n2 = 0
    for n, c in enumerate(s[st:]):
        n1 += c in p1
        n2 += c in p2
        if n1 and n1 == n2:
            return st + n


def bytes_format(data, n=16):
    '''TEST: bytes_format(bytes(range(128)))'''
    s = ''.join('\\x%02x' % c for c in data)
    return "(b'%s')" % "'\n b'".join(s[i:i+n*4] for i in range(0, len(s), n * 4))


def bytes_print(data, n=16):
    print(bytes_format(data, n))


def bytes_hex(data, offset=0, length=-1, slice=-1):
    s = ' '.join('%02X' % c for c in data)
    s = ['%08X ' % i + s[i*3:(i+16)*3] for i in range(0, len(data), 16)]
    s = '\n'.join(s)
    return s


def install(path, block=False):
    p = os.popen('pip install "%s"' % path)
    if block:
        return p.read()


def input_wait(msg):
    while input(msg + '[y/n]: ').lower() != 'y':
        pass


input_default = lambda msg, default: input('input <%s>, keep <%s> press enter: ' % (msg, default)) or default


class Catch:
    def __init__(self, log='log.txt'):
        self.log = log

    def __enter__(self):
        pass

    def __exit__(self, *args):
        if any(args):
            traceback.print_exc()
            error = traceback.format_exc()
            tt = time.strftime('[%Y-%m-%d %H:%M:%S] ')
            with open(self.log, 'a', encoding='u8') as f:
                f.write(tt + error + '\n')
        return True


catch = Catch()


__all__ = [k for k in globals() if k not in __all__]
