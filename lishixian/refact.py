import os
from functools import partial
from contextlib import suppress

join = os.path.join
makedirs = partial(os.makedirs, exist_ok=True)
# open = partial(open, encoding='u8')


def split(p):
    root, file = os.path.split(p)
    name, ext = os.path.splitext(file)
    return root, name, ext


def walk(path, exts=()):
    for root, folders, files in os.walk(path):
        for file in files:
            if not exts or os.path.splitext(file)[1] in exts:
                yield os.path.join(root, file)


_open = open


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
