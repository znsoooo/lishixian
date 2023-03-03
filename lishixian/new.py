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
infinity = itertools.count
makedirs = partial(os.makedirs, exist_ok=True)
breakpoint = lambda: pdb.set_trace()
# open = partial(open, encoding='u8')
popen = lambda cmd: subprocess.Popen(cmd, -1, None, -1, -1, -1, shell=True).stdout
listdir = lambda *paths: os.listdir(os.path.join(*paths))
findall = lambda pattern, string, flags=0: [(m.start(), m.end(), m.group()) for m in re.finditer(pattern, string, flags)]
split = lambda arr, cols: [arr[i:i+cols] for i in range(0, len(arr), cols)]


def detect(file):
    import chardet
    with _open(file, 'rb') as f:
        b = f.read()
    return chardet.detect(b)['encoding'] or 'utf-8'


def walk(paths, exts=''):
    paths = paths if isinstance(paths, (list, tuple)) else [paths]
    exts = [exts] if isinstance(exts, str) else exts
    exts = [ext.lower() for ext in exts]
    for path in paths:
        if os.path.isfile(path):
            if any(path.lower().endswith(ext) for ext in exts):
                yield path
        for root, folders, files in os.walk(path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in exts):
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
        root = os.path.dirname(self.p)
        if root and not os.path.exists(root):
            os.makedirs(root)
        if isinstance(data, bytes):
            mode += 'b'
        with _open(self.p, mode, encoding='u8') as f:
            f.write(data)

    def append(self, data):
        self.write(data, 'a')


__all__ = [k for k in globals() if k not in __all__]
