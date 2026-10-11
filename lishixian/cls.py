"""Useful Classes"""

import re
import ctypes
import socket
import struct
import threading
import configparser
from io import BytesIO


__all__ = list(globals())


class Config:
    def __init__(self, path, section='default', encoding='u8'):
        self._data = {}
        self._path = path
        self._section = section
        self._encoding = encoding

    def __iter__(self):
        yield from self.data

    def __len__(self):
        return len(self.data)

    def __contains__(self, name):
        return name in self.data

    def __delattr__(self, name):
        if name in self.data:
            del self.data[name]
            self.save()

    def __getattr__(self, name):
        if name in self.data:
            return self.data[name]

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self.data[name] = value
            self.save()

    def __repr__(self):
        return '''Config('%s', '%s', '%s')%s''' % (
            self._path, self._section, self._encoding,
            ''.join('\n.%s=%s' % item for item in self.data.items()))

    @property
    def data(self):
        p = configparser.ConfigParser()
        p.read(self._path, encoding=self._encoding)
        if not p.has_section(self._section):
            p.add_section(self._section)
        self._data = dict(p.items(self._section))
        return self._data

    def save(self):
        p = configparser.ConfigParser()
        p.read_dict({self._section: self._data})
        with open(self._path, 'w', encoding=self._encoding) as f:
            p.write(f, False)


class Thread(threading.Thread):
    def __init__(self, target, *args, **kwargs):
        threading.Thread.__init__(self, target=target, args=args, kwargs=kwargs)

        self.result = None
        self.finish = False

        self.start()

    def run(self):
        self.result = self._target(*self._args, **self._kwargs)
        self.finish = True

    def stop(self):
        if not self.finish:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(self.ident, ctypes.py_object(SystemExit))


class Tcp:
    def __init__(self, addr, port):
        self.host = not addr
        self.addr = addr
        self.port = port
        self.connect()

    def connect(self):
        if self.host:
            self.server = socket.socket()
            self.server.bind(('', self.port))
            self.server.listen(5)
            self.client, (addr, port) = self.server.accept()
        else:
            self.client = socket.socket()
            self.client.connect((self.addr, self.port))

    def close(self):
        self.client.close()
        if self.host:
            self.server.close()

    def send(self, data):
        data = data.encode() if isinstance(data, str) else data
        self.client.sendall(data)

    def recv(self, length):
        return self.client.recv(length)

    def sendrecv(self, data, size):
        return [self.send(data), self.recv(size)][1]

    def recvsend(self, size, data):
        return [self.recv(size), self.send(data)][0]

    def sendlong(self, data):
        data = data.encode() if isinstance(data, str) else data
        assert len(data) < 1 << 32  # max 4GB
        self.send(struct.pack('I', len(data)) + data)

    def recvlong(self):
        length = struct.unpack('I', self.recv(4))[0]  # max 4GB
        data = bytearray()
        while len(data) < length:
            chunk = self.client.recv(length - len(data))
            if not chunk:
                raise ConnectionError
            data.extend(chunk)
        return bytes(data)


class Udp:
    def __init__(self, addr, port):
        self.host = not addr
        self.addr = addr
        self.port = port
        self.buffsize = 64000
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if self.host:
            self.s.bind(('', port))

    def close(self):
        self.s.close()

    def send(self, data):
        data = data.encode() if isinstance(data, str) else data
        self.s.sendto(data, (self.addr, self.port))

    def recv(self, size):
        data, (self.addr, self.port) = self.s.recvfrom(size)
        return data

    def sendrecv(self, data, size):
        return [self.send(data), self.recv(size)][1]

    def recvsend(self, size, data):
        return [self.recv(size), self.send(data)][0]

    def sendlong(self, data):
        data = data.encode() if isinstance(data, str) else data
        count = -(-len(data) // self.buffsize)
        self.send(struct.pack('I', count))
        self.recv(4)
        f = BytesIO(data)
        for i in range(count):
            self.send(f.read(self.buffsize))
            self.recv(4)

    def recvlong(self):
        count = struct.unpack('I', self.recv(4))[0]
        self.send(b'echo')
        data = bytearray()
        for i in range(count):
            data.extend(self.recv(self.buffsize))
            self.send(b'echo')
        return bytes(data)


class Table(list):
    def __getitem__(self, key):
        if isinstance(key, str):
            return self[key, :]
        elif isinstance(key, tuple):
            row_key, col_key = key
            if isinstance(row_key, str):
                row_key = self[:, 0].index(row_key)
            if isinstance(col_key, str):
                col_key = self[0].index(col_key)
            rows_data = self[row_key]
            if isinstance(row_key, int):
                return rows_data[col_key]
            elif isinstance(row_key, slice):
                result = [row[col_key] for row in rows_data]
                return Table(result) if isinstance(col_key, slice) else result
        result = super().__getitem__(key)
        return Table(result) if isinstance(key, slice) else result

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            row_key, col_key = key
            if isinstance(row_key, str):
                row_key = self[:, 0].index(row_key)
            if isinstance(col_key, str):
                col_key = self[0].index(col_key)
            rows_data = self[row_key]
            if isinstance(row_key, int):
                rows_data[col_key] = value
            elif isinstance(row_key, slice):
                for row, row_value in zip(rows_data, value):
                    row[col_key] = row_value
            self[row_key] = rows_data
        else:
            super().__setitem__(key, value)

    def __invert__(self):
        return Table([[row[c] for row in self] for c in range(len(self[0]))])

    def __contains__(self, other):
        return any(other in row for row in self)

    def __add__(self, other):
        return Table(list(self) + list(other))

    def __or__(self, other):
        data = self.copy()
        for r, row in enumerate(other):
            data[r].extend(row)
        return Table(data)

    def __repr__(self):
        return '[%s]' % ',\n '.join(map(str, self))

    def copy(self):
        return self[:, :]

    def rappend(self, row):
        self.rinsert(self.rows(), row)

    def cappend(self, col):
        self.cinsert(self.cols(), col)

    def rextend(self, rows):
        [self.rappend(row) for row in rows]

    def cextend(self, cols):
        [self.cappend(col) for col in cols]

    def rindex(self, header):
        return header if isinstance(header, int) else self[:, 0].index(header)

    def cindex(self, header):
        return header if isinstance(header, int) else self[0, :].index(header)

    def rinsert(self, idx, row):
        idx = self.rindex(idx)
        self.insert(idx, row)

    def cinsert(self, idx, col):
        idx = self.cindex(idx)
        [row.insert(idx, val) for row, val in zip(self, col)]

    def rpop(self, idx=-1):
        idx = self.rindex(idx)
        return self.pop(idx)

    def cpop(self, idx=-1):
        idx = self.cindex(idx)
        return [row.pop(idx) for row in self]

    def index(self, val):
        for r, row in enumerate(self):
            for c, value in enumerate(row):
                if val == value:
                    return (r, c)
        raise ValueError('%r is not in table' % val)

    def count(self, val):
        return sum(row.count(val) for row in self)

    def rows(self):
        return len(self[:, 0])

    def cols(self):
        return len(self[0, :])


class Re(str):
    class Match:
        def __init__(self, match):
            self.m = match

        def __bool__(self):
            return bool(self.m)

        def __repr__(self):
            return repr(self.m)

        def __getitem__(self, group):
            if not isinstance(group, tuple):
                group = group,
            return Re.Wash(self.m.group(*group))

        def expand(self, template):
            return Re.Wash(self.m.expand(template))

        def group(self, *group):
            return Re.Wash(self.m.group(*group))

        def groups(self, default=None):
            return Re.Wash(self.m.groups(default))

        def groupdict(self, default=None):
            return Re.Wash(self.m.groupdict(default))

        def start(self, group=0):
            return self.m.start(group)

        def end(self, group=0):
            return self.m.end(group)

        def span(self, group=0):
            return self.m.span(group)

    @staticmethod
    def Wash(value):
        if isinstance(value, Re):
            return value
        if isinstance(value, str):
            return Re(value)
        if isinstance(value, (list, tuple, set)):
            return type(value)(Re.Wash(v) for v in value)
        if isinstance(value, dict):
            return {Re.Wash(k): Re.Wash(v) for k, v in value.items()}
        return value

    def reflags(self, flags):
        if isinstance(flags, int):
            return flags
        result = 0
        for ch in flags.upper():
            result |= getattr(re, ch)
        return result

    def rematch(self, pattern, flags='m'):
        flags = self.reflags(flags)
        m = re.match(pattern, self, flags)
        return Re.Match(m)

    def refullmatch(self, pattern, flags='m'):
        flags = self.reflags(flags)
        m = re.fullmatch(pattern, self, flags)
        return Re.Match(m)

    def research(self, pattern, flags='m'):
        flags = self.reflags(flags)
        m = re.search(pattern, self, flags)
        return Re.Match(m)

    def resub(self, pattern, repl, count=0, flags='m'):
        flags = self.reflags(flags)
        new_str = re.sub(pattern, repl, self, count=count, flags=flags)
        return Re(new_str)

    def resubn(self, pattern, repl, count=0, flags='m'):
        flags = self.reflags(flags)
        new_str, n = re.subn(pattern, repl, self, count=count, flags=flags)
        return Re(new_str), n

    def resplit(self, pattern, maxsplit=0, flags='m'):
        flags = self.reflags(flags)
        parts = re.split(pattern, self, maxsplit=maxsplit, flags=flags)
        return [Re(p) for p in parts]

    def refind(self, pattern, flags='m'):
        return self.refindall(pattern, flags)[0]

    def refindall(self, pattern, flags='m'):
        flags = self.reflags(flags)
        return Re.Wash(re.findall(pattern, self, flags))

    def refinditer(self, pattern, flags='m'):
        flags = self.reflags(flags)
        for m in re.finditer(pattern, self, flags):
            yield Re.Match(m)

    def __add__(self, other):
        return Re(super().__add__(other))

    def __radd__(self, other):
        return Re(other + str(self))

    def __mul__(self, other):
        return Re(super().__mul__(other))

    def __rmul__(self, other):
        return Re(super().__rmul__(other))

    def __mod__(self, other):
        return Re(super().__mod__(other))

    def __getitem__(self, index):
        return Re(super().__getitem__(index))

    def lower(self):
        return Re(super().lower())

    def upper(self):
        return Re(super().upper())

    def strip(self, chars=None):
        return Re(super().strip(chars))

    def lstrip(self, chars=None):
        return Re(super().lstrip(chars))

    def rstrip(self, chars=None):
        return Re(super().rstrip(chars))

    def replace(self, old, new, count=-1):
        return Re(super().replace(old, new, count))

    def split(self, sep=None, maxsplit=-1):
        parts = super().split(sep, maxsplit)
        return [Re(p) for p in parts]

    def rsplit(self, sep=None, maxsplit=-1):
        parts = super().rsplit(sep, maxsplit)
        return [Re(p) for p in parts]

    def splitlines(self, keepends=False):
        lines = super().splitlines(keepends)
        return [Re(line) for line in lines]

    def join(self, iterable):
        return Re(super().join(iterable))


__all__ = [k for k in globals() if k not in __all__]


if __name__ == '__main__':
    import time

    def ThreadFunction(timeout, fun, *args, **kwargs):
        t = Thread(fun, *args, **kwargs)
        t.join(timeout)
        t.stop()
        return t.result

    def f():
        for i in range(3):
            time.sleep(1)
            print(i)
        return 9

    print(ThreadFunction(0.5, f))
    print(ThreadFunction(1.5, f))
    print(ThreadFunction(3.5, f))
