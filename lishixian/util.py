"""Useful Functions with Built-in Library"""

import os
import html
import time
import traceback
import urllib.parse
import urllib.request


__all__ = list(globals())


# ---------------------------------------------------------------------------
# Debug
# ---------------------------------------------------------------------------


pause = lambda: input('Press enter to continue: ')


def log(*value, file='log.txt'):
    string = ' '.join(map(str, value)) + '\n'
    header = time.strftime('[%Y-%m-%d %H:%M:%S] ')
    print(string, end='')
    with open(file, 'a', encoding='u8') as f:
        f.write(header + string)


_last = 0
def progress(*value, interval=1):
    global _last
    now = time.time()
    if interval == 0 or now - _last > interval:
        _last = now
        print(*value)


def check(obj, patt='.*', stdout=True):
    import re
    import sys
    import inspect
    patt = re.compile(patt)
    stdout = {True: sys.stdout, False: sys.stderr}.get(stdout, stdout)
    print('obj: %r' % obj, end='')
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
            print('\n' + key, end='')
            print(result, file=stdout, end='')
    print()


_fps_n = -1
_fps_t1 = 0
def fps():
    import time
    global _fps_n, _fps_t1
    _fps_n += 1
    fps_t2 = time.time()
    if _fps_t1 == 0:
        _fps_t1 = fps_t2
    if fps_t2 - _fps_t1 > 1:
        print('fps: %.1f' % (_fps_n / (fps_t2 - _fps_t1)))
        _fps_t1 = fps_t2
        _fps_n = 0
    return True


_count_dict = {}
def count(value=None, target=None):
    if value not in _count_dict:
        _count_dict[value] = 0
    if target is None or value == target:
        _count_dict[value] += 1
    return _count_dict[value]


def recent(iterable, max=0):
    history = []
    for item in iterable:
        history.append(item)
        yield history
        if len(history) == max:
            history.pop(0)


def parser2opt(parser, opt='opt'):
    actions = parser._actions[1:]
    w1 = max(len(ac.dest) for ac in actions)
    w2 = max(len(repr(ac.default)) for ac in actions)
    for ac in actions:
        print('%s.%s = %s  # %s' % (opt, ac.dest.ljust(w1), repr(ac.default).ljust(w2), ac.help))


# ---------------------------------------------------------------------------
# File system
# ---------------------------------------------------------------------------


ext = lambda p: os.path.splitext(p)[1].lower()
stem = lambda p: os.path.splitext(os.path.basename(p))[0]
select = lambda path: os.popen('explorer /select, "%s"' % os.path.abspath(path))


def path_mark(path, mark='.bak'):
    root, ext = os.path.splitext(path)
    return root + mark + ext


def path_safe(p, repl=None):  # not include path
    from urllib.parse import quote_plus
    map = {ord(c): quote_plus(c) if repl is None else repl for c in '\r\n\t\\/:*?"<>|'}
    return p.translate(map)


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


def file_mtime(path):
    mtime = os.stat(path).st_mtime
    return time.localtime(mtime)[:6]


def file_ctime(path):
    ctime = os.stat(path).st_ctime
    return time.localtime(ctime)[:6]


def file_utime(path, date):
    mtime = time.mktime((tuple(date) + (0,) * 6)[:9])
    os.utime(path, (mtime, mtime))


# ---------------------------------------------------------------------------
# Math
# ---------------------------------------------------------------------------


def factorize(num):
    import math
    divisor = 2
    while divisor <= math.sqrt(num):
        if num % divisor == 0:
            print(divisor, '*', end=' ')
            num //= divisor
        else:
            divisor += 1
    print(num)


def primes(max):
    ps = []
    for n in range(2, max):
        if all(n % p for p in ps):
            ps.append(n)
    return ps


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


def scan(format, string):
    import re
    sp = re.split('(%d|%f|%s)', format, flags=re.I)
    patt = ''.join('(.*)' if i % 2 else re.escape(s) for i, s in enumerate(sp))
    match = re.fullmatch(patt, string)
    fun_map = {'%d': int, '%f': float, '%s': str}
    formats = re.findall('%d|%f|%s', format, flags=re.I)
    return [fun_map[fmt.lower()](s) for fmt, s in zip(formats, match.groups())]


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