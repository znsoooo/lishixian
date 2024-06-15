"""Useful Classes"""

import ctypes
import threading
import configparser


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
    import socket
    import struct

    def __init__(self, addr, port):
        self.host = not addr
        self.addr = addr
        self.port = port
        self.connect()

    def connect(self):
        if self.host:
            self.server = self.socket.socket()
            self.server.bind(('', self.port))
            self.server.listen(5)
            self.client, (addr, port) = self.server.accept()
        else:
            self.client = self.socket.socket()
            self.client.connect((self.addr, self.port))

    def close(self):
        self.client.close()
        if self.host:
            self.server.close()

    def send(self, data):
        data = data.encode() if isinstance(data, str) else data
        self.client.send(data)

    def recv(self, length):
        return self.client.recv(length)

    def sendrecv(self, data, size):
        return [self.send(data), self.recv(size)][1]

    def recvsend(self, size, data):
        return [self.recv(size), self.send(data)][0]

    def sendlong(self, data):
        data = data.encode() if isinstance(data, str) else data
        assert len(data) < 1 << 32  # max 4GB
        self.client.send(self.struct.pack('I', len(data)) + data)

    def recvlong(self):
        length = self.struct.unpack('I', self.recv(4))[0]  # max 4GB
        data = bytearray()
        while len(data) < length:
            data.extend(self.client.recv(length - len(data)))
        return bytes(data)


class Udp:
    import socket
    import struct
    from io import BytesIO

    def __init__(self, addr, port):
        self.host = not addr
        self.addr = addr
        self.port = port
        self.buffsize = 64000
        self.s = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_DGRAM)
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
        self.send(self.struct.pack('I', count))
        self.recv(4)
        f = self.BytesIO(data)
        for i in range(count):
            self.send(f.read(self.buffsize))
            self.recv(4)

    def recvlong(self):
        count = self.struct.unpack('I', self.recv(4))[0]
        self.send(b'echo')
        data = bytearray()
        for i in range(count):
            data.extend(self.recv(self.buffsize))
            self.send(b'echo')
        return bytes(data)


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
