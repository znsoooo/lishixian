"""Useful Functions with Built-in Library"""

import os
import html
import time
import base64
import traceback
import urllib.parse


__all__ = list(globals())


# ---------------------------------------------------------------------------
# Debug
# ---------------------------------------------------------------------------


def log(*value, file='log.txt'):
    string = ' '.join(map(str, value)) + '\n'
    prefix = time.strftime('[%Y-%m-%d %H:%M:%S] ')
    print(string, end='')
    with open(file, 'a', encoding='u8') as f:
        f.write(prefix + string)


def redirect(file='log.txt', prefix='[%Y-%m-%d %H:%M:%S]'):
    def log_write(text):
        nonlocal newline, prefix_last
        lock.acquire()
        prefix_text = time.strftime(prefix)
        prefix_blank = ' ' * len(prefix_text)
        with open(file, 'a', encoding='u8') as f:
            for line in text.splitlines(True):
                if newline:
                    if prefix_last != prefix_text:
                        prefix_last = prefix_text
                        f.write(prefix_text + ' | ')
                    else:
                        f.write(prefix_blank + ' | ')
                f.write(line)
                newline = line[-1:] in '\r\n'
        lock.release()

    import sys
    from threading import Lock

    newline = True
    prefix_last = None
    lock = Lock()

    stdout_write = sys.stdout.write
    stderr_write = sys.stderr.write
    sys.stdout.write = lambda text: [stdout_write(text), log_write(text)]
    sys.stderr.write = lambda text: [stderr_write(text), log_write(text)]


def sudo():
    import sys, ctypes
    if not ctypes.windll.shell32.IsUserAnAdmin():
        args = ' '.join('"' + arg + '"' for arg in sys.argv)
        ok = ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, args, None, 1) > 32
        exit()


def kill(ths=None):
    import re, ctypes, threading
    if isinstance(ths, int):  # find as ident
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ths, ctypes.py_object(SystemExit))
    elif isinstance(ths, threading.Thread):  # find as Thread object
        kill(ths.ident)
    elif isinstance(ths, str):  # find as pattern
        for th in threading.enumerate():
            if re.fullmatch(ths, th.name):
                kill(th.ident)
    elif isinstance(ths, (list, tuple)):  # iterate finding
        for th in ths:
            kill(th)
    elif ths is None:  # kill all but main
        main = threading.main_thread()
        for th in threading.enumerate():
            if th is not main and th.name != 'SockThread':  # IDLE Thread name is 'SockThread'
                kill(th.ident)
    else:
        raise TypeError(type(ths))


def check(obj, patt='.*', stdout=True):
    import re, sys, inspect, traceback
    patt = re.compile(patt)
    stdout = {True: sys.stdout, False: sys.stderr}.get(stdout, stdout)
    print('obj: %r' % obj, end='')
    for key in sorted(dir(obj)):
        if patt.fullmatch(key):
            print('\n.' + key, end='')
            try:
                attr = getattr(obj, key)  # getter might raise error
                try:
                    print(inspect.signature(attr), end='')
                except Exception:
                    pass
                result = repr(attr() if callable(attr) else attr)
            except Exception:
                result = traceback.format_exc(0).strip()
            print(' = ' + result, file=stdout, end='')
    print()


def varname(var):
    import inspect
    frame = inspect.currentframe()
    frames = []
    while frame:
        frames.append(frame)
        frame = frame.f_back
    for frame in reversed(frames):
        for key, value in reversed(list(frame.f_locals.items())):  # find last location
            if value is var:
                return key


def imports(path):
    import os, sys, importlib.util
    name = os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


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


_clock_start = None
def clock(reset=False):
    global _clock_start
    if _clock_start is None or reset:
        _clock_start = time.time()
    return time.time() - _clock_start


_timer_start = _timer_end = time.time()
def timer(reset=True):
    global _timer_start, _timer_end
    _timer_end = time.time()
    ret = _timer_end - _timer_start
    if reset:
        _timer_start = _timer_end
    return ret


_progress_last = 0
def progress(*value, interval=1):
    global _progress_last
    now = time.time()
    if interval == 0 or now - _progress_last > interval:
        _progress_last = now
        print(*value)


_fps_n = -1
_fps_t1 = 0
def fps():
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


def recent(iterable, max=0, strict=False):
    history = []
    for item in iterable:
        history.append(item)
        if not strict or len(history) == max:
            yield tuple(history)
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


def copy(src, dst, overwrite=True):
    import os, shutil
    osp = os.path
    os.makedirs(dst if osp.isdir(src) else osp.dirname(dst), exist_ok=True)
    if osp.isdir(src):
        for name in os.listdir(src):
            copy(osp.join(src, name), osp.join(dst, name), overwrite)
    elif overwrite or not osp.exists(dst):
        shutil.copy2(src, dst)


def move(src, dst, overwrite=True):
    import os
    osp = os.path
    os.makedirs(dst if osp.isdir(src) else osp.dirname(dst), exist_ok=True)
    if osp.isdir(src):
        for name in os.listdir(src):
            move(osp.join(src, name), osp.join(dst, name), overwrite)
        if not os.listdir(src):
            os.rmdir(src)
    elif overwrite or not osp.exists(dst):
        if osp.exists(dst):
            os.remove(dst)
        os.rename(src, dst)


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
    primes = []
    for num in range(2, max):
        if all(num % prime for prime in primes):
            primes.append(num)
    return primes


def randlog(min, max):
    import math, random
    min, max = sorted([min, max])
    log_min = math.log(min)
    log_max = math.log(max)
    rand_log = random.uniform(log_min, log_max)
    return math.exp(rand_log)


# ---------------------------------------------------------------------------
# Web
# ---------------------------------------------------------------------------


escape = html.escape
unescape = html.unescape
quote = urllib.parse.quote_plus  # quote every word include '/'
unquote = urllib.parse.unquote
b64encode = lambda s: base64.b64encode(s).decode()
b64decode = lambda s: base64.b64decode(s + '==')


def urlopen(url, base='', query=None, fragment=None, data=None, headers=None, method=None, retry=1, timeout=10, strict=True):
    import re, urllib.parse, urllib.request
    url = urllib.parse.urljoin(base, url)
    url += '?' + urllib.parse.urlencode(query) if query else ''
    url += '#' + str(fragment) if fragment else ''
    data = data.encode() if isinstance(data, str) else data
    headers = headers or {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'}
    headers = dict(re.findall(r'^\s*(.*?)\s*:\s*(.*?)\s*$', headers, re.M)) if isinstance(headers, str) else headers
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
    def __init__(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            return True
        traceback.print_exc()
        return exc_type is not KeyboardInterrupt


catch = Catch()


__all__ = [k for k in globals() if k not in __all__]
