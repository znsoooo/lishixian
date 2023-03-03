"""Useful Classes"""

import ctypes
import socket
import struct
import configparser
from threading import Thread as _Thread


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


class Thread(_Thread):
    def __init__(self, target, *args, **kwargs):
        _Thread.__init__(self, target=target, args=args, kwargs=kwargs)

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
        if isinstance(data, str):
            data = data.encode()
        self.client.send(data)

    def recv(self, length):
        return self.client.recv(length)

    def send_with_header(self, data):
        if isinstance(data, str):
            data = data.encode()
        assert len(data) < 1 << 32  # max 4GB
        self.client.send(struct.pack('I', len(data)) + data)

    def recv_with_header(self):
        length = struct.unpack('I', self.recv(4))[0]  # max 4GB
        s = bytearray()
        while len(s) < length:
            s.extend(self.client.recv(length - len(s)))
        return bytes(s)


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

