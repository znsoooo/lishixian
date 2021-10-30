import os
import html
import threading
import time
import urllib.parse
import urllib.request

from .refact import print

# LOG = time.strftime('RECORD_%Y%m%d_%H%M%S.log')
LOG = time.strftime('LOG_%Y%m%d_%H%M%S.txt')


# ---------------------------------------------------------------------------
# Debug
# ---------------------------------------------------------------------------


def tag():
    return time.strftime('[%Y-%m-%d %H:%M:%S] ')


def log(*value):
    s = tag() + print(*value)
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


def install(path):
    os.popen('pip install "%s"' % path)


def input_wait(msg):
    while input(msg + '[y/n]: ').lower() != 'y':
        pass


input_default = lambda msg, default: input('input <%s>, keep <%s> press enter: ' % (msg, default)) or default


class MultiThread:
    def __init__(self, max):
        self.cnt = threading.BoundedSemaphore(max)

    def append(self):
        self.cnt.acquire()

    def pop(self):
        self.cnt.release()
