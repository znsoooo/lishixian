"""Useful Functions with Built-in Library"""

import os
import html
import time
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


def check(obj, patt='.*'):
    import re
    import sys
    import inspect
    patt = re.compile(patt)
    print('\nobj:', obj)
    for key in sorted(dir(obj)):
        attr = getattr(obj, key)
        try:
            key += str(inspect.signature(attr))
        except (TypeError, ValueError):
            pass
        if patt.fullmatch(key):
            key = '.' + key
            if not callable(attr):
                result = repr(attr)
                key += ' = '
            else:
                try:
                    result = repr(attr())
                    key += ' = '
                except Exception:
                    result = ''
            print(key, end='')
            print(result, file=sys.stderr)


fps_n = -1
fps_t1 = 0
def fps():
    import time
    global fps_n, fps_t1
    fps_n += 1
    fps_t2 = time.time()
    if fps_t1 == 0:
        fps_t1 = fps_t2
    if fps_t2 - fps_t1 > 1:
        print('fps: %.1f' % (fps_n / (fps_t2 - fps_t1)))
        fps_t1 = fps_t2
        fps_n = 0
    return True


# ---------------------------------------------------------------------------
# File system
# ---------------------------------------------------------------------------


stem = lambda p: os.path.splitext(os.path.basename(p))[0]
select = lambda path: os.popen('explorer /select, "%s"' % os.path.abspath(path))


def path_mark(path, mark='.bak'):
    root, ext = os.path.splitext(path)
    return root + mark + ext


def path_quote(p, repl=None):  # not include path
    for c in '\r\n\t\\/:*?"<>|':
        new = repl if repl is not None else urllib.parse.quote_plus(c)
        p = p.replace(c, new)
    return p


def path_split(p):
    root, file = os.path.split(p)
    name, ext = os.path.splitext(file)
    return root, name, ext


def path_unique(p, dash='-'):
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
