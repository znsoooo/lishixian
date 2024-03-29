"""Useful Functions with Built-in Library"""

import os
import html
import time
import traceback
import urllib.parse


__all__ = list(globals())


# ---------------------------------------------------------------------------
# Debug
# ---------------------------------------------------------------------------


def log(*value, file='log.txt'):
    string = ' '.join(map(str, value)) + '\n'
    header = time.strftime('[%Y-%m-%d %H:%M:%S] ')
    print(string, end='')
    with open(file, 'a', encoding='u8') as f:
        f.write(header + string)


def sudo():
    import sys, ctypes
    if not ctypes.windll.shell32.IsUserAnAdmin():
        args = ' '.join('"' + arg + '"' for arg in sys.argv)
        ok = ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, args, None, 1) > 32
        exit()


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


def print_paths():
    import os, sys, inspect
    print('\nEXE:\n  ' + sys.executable)
    print('\nWORK:\n  ' + os.getcwd())
    print('\nPATH:\n  ' + '\n  '.join(sys.path))
    print('\nFILE:\n  ' + inspect.currentframe().f_back.f_globals['__file__'])
    print('\nARGS:\n  ' + '\n  '.join(sys.argv))


def print_lines(lines):
    print('\n'.join(map(str, lines)))


def print_table(table):
    cols = max(len(row) for row in table)
    table = [[str(cell) for cell in row] + [''] * (cols - len(row)) for row in table]
    widths = [max(len(item) for item in column) for column in zip(*table)]
    for row in table:
        line = [item.ljust(width) for item, width in zip(row, widths)]
        print(' | '.join(line))


_last = 0
def progress(*value, interval=1):
    global _last
    now = time.time()
    if interval == 0 or now - _last > interval:
        _last = now
        print(*value)


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
def count(add=1, name='default'):
    _count_dict[name] = _count_dict.get(name, 0) + add
    return _count_dict[name]


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


p1 = dirname = lambda path, new='': os.path.join(os.path.dirname(path), new)
p2 = stem = lambda path: os.path.splitext(os.path.basename(path))[0]
p3 = ext = lambda path: os.path.splitext(path)[1].lower()
p12 = root = lambda path, new='': os.path.splitext(path)[0] + new
p23 = basename = lambda path, new='': os.path.join(new, os.path.basename(path))
p123 = lambda path, new='': os.path.splitext(path)[0] + new + os.path.splitext(path)[1]

select = lambda p: os.popen('explorer /select, "%s"' % os.path.abspath(p))

file_mtime = lambda path: time.localtime(os.stat(path).st_mtime)[:6]
file_ctime = lambda path: time.localtime(os.stat(path).st_ctime)[:6]
file_utime = lambda path, date: os.utime(path, (time.mktime((tuple(date) + (0,) * 6)[:9]),) * 2)

path_mark = lambda path, mark='.bak': '{0}{2}{1}'.format(*(os.path.splitext(path) + (mark,)))
path_safe = lambda path, repl=None: path.translate({ord(c): urllib.parse.quote_plus(c) if repl is None else repl for c in '\r\n\t\\/:*?"<>|'})
path_split = lambda path: (os.path.dirname(path),) + os.path.splitext(os.path.basename(path))


def path_unique(path, dash='-', start=2):
    root, ext = os.path.splitext(path)
    while os.path.exists(path):
        path = '%s%s%d%s' % (root, dash, start, ext)
        start += 1
    return path


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


def urlopen(url, base='', query=None, fragment=None, data=None, headers=None, method=None, retry=1, timeout=10, strict=True):
    import re, urllib.parse, urllib.request
    headers = headers or {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'}
    url = urllib.parse.urljoin(base, url)
    url += '?' + urllib.parse.urlencode(query) if query else ''
    url += '#' + str(fragment) if fragment else ''
    data = data.encode() if isinstance(data, str) else data
    headers = dict(re.findall(r'(.*?):\s*(.*)', headers)) if isinstance(headers, str) else headers
    request = urllib.request.Request(url, data, headers, method=method)
    for i in range(retry - 1):
        try:
            return urllib.request.urlopen(request, timeout=timeout).read()
        except Exception:
            pass
    try:
        return urllib.request.urlopen(request, timeout=timeout).read()
    except UserWarning if strict else Exception:
        return b''


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


def findpair(text, pair='()', start=0):
    n1 = n2 = 0
    for n, c in enumerate(text[start:]):
        n1 += c in pair[0]
        n2 += c in pair[1]
        if n1 and n1 == n2:
            return start + n


def install(path):
    import pip
    pip.main(['install', path])


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
