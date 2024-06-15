"""Rewrite Existing Functions"""

import os
import re
import pdb
import sys
import random
import struct
import builtins
import itertools
import subprocess


__all__ = list(globals())


print = lambda *value, file=True: builtins.print(' '.join(map(str, value)) + '\n', end='', file={True: sys.stdout, False: sys.stderr}.get(file, file))
loop = itertools.count
randbytes = lambda n: builtins.bytes(random.randint(0, 255) for i in range(n))
breakpoint = lambda: pdb.set_trace()
popen = lambda cmd: subprocess.Popen(cmd, -1, None, -1, -1, -1, shell=True).stdout
listdir = lambda *paths: os.listdir(os.path.join(*paths))
findall = lambda pattern, string, flags=0: [(m.start(), m.end(), m.group()) for m in re.finditer(pattern, string, flags)]
split = lambda arr, cols: [arr[i:i+cols] for i in range(0, len(arr), cols)]
pack = lambda fmt, values: struct.pack(fmt, *values)
unpack = lambda fmt, string: struct.unpack_from(fmt, string) + (string[struct.calcsize(fmt):],)


def detect(path):
    import chardet
    with builtins.open(path, 'rb') as f:
        b = f.read()
    return chardet.detect(b)['encoding'] or 'utf-8'


def walk(paths='.', exts=''):
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


def bytes(data, width=16):
    s = ''.join('\\x%02x' % c for c in data)
    s = "(b'%s')" % "'\n b'".join(s[i: i + width * 4] for i in range(0, len(s), width * 4))
    return s if len(data) > width else s.strip('()')


def memoryview(data, width=16, offset=0):
    s = ' '.join('%02X' % c for c in data)
    return '\n'.join('%08X ' % (i + offset) + s[i * 3: (i + width) * 3] for i in range(0, len(data), width))


__all__ = [k for k in globals() if k not in __all__]
