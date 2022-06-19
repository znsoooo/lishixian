"""Rewrite Existing Functions"""

import os
import re
import pdb
import sys
import itertools
import subprocess
from functools import partial
from contextlib import suppress

_open = open


__all__ = list(globals())


_print, print = print, lambda *value, file=sys.stdout: _print(' '.join(map(str, value)) + '\n', end='', file=file)
join = os.path.join
infinity = itertools.count
makedirs = partial(os.makedirs, exist_ok=True)
breakpoint = lambda: pdb.set_trace()
# open = partial(open, encoding='u8')
popen = lambda cmd: subprocess.Popen(cmd, -1, None, -1, -1, -1, shell=True).stdout
listdir = lambda *paths: os.listdir(os.path.join(*paths))
findall = lambda pattern, string, flags=0: [(m.start(), m.end(), m.group()) for m in re.finditer(pattern, string, flags)]
split = lambda arr, cols: [arr[i:i+cols] for i in range(0, len(arr), cols)]


def splitpath(p):
    root, file = os.path.split(p)
    name, ext = os.path.splitext(file)
    return root, name, ext


def walk(path, exts=()):
    if os.path.isfile(path):
        if not exts or os.path.splitext(path)[1] in exts:
            yield os.path.abspath(path)
    for root, folders, files in os.walk(path):
        for file in files:
            if not exts or os.path.splitext(file)[1] in exts:
                yield os.path.join(root, file)


class open:
    def __init__(self, file):
        self.p = file

    def read(self):
        if not os.path.isfile(self.p):
            return None
        with suppress(UnicodeDecodeError):
            with _open(self.p, encoding='u8') as f:
                return f.read()
        with suppress(UnicodeDecodeError):
            with _open(self.p, encoding='gbk') as f:
                return f.read()
        with _open(self.p, 'rb') as f:
            return f.read()

    def write(self, data, mode='w'):
        os.makedirs(os.path.dirname(self.p), exist_ok=True)
        if isinstance(data, bytes):
            mode += 'b'
        with _open(self.p, mode, encoding='u8') as f:
            f.write(data)

    def append(self, data):
        self.write(data, 'a')


__all__ = [k for k in globals() if k not in __all__]
