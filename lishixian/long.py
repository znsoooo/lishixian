import ctypes
import configparser
from threading import Thread


__all__ = list(globals())


class MyConfigParser(configparser.ConfigParser):
    def __init__(self, path, section):
        configparser.ConfigParser.__init__(self)
        self.path = path
        self.s = section
        self.read(path)
        if not self.has_section(section):
            self.add_section(section)

    def getkey(self, key, default=None):
        self.read(self.path)
        if self.has_option(self.s, key):
            return self.get(self.s, key)
        elif default:
            self.set(self.s, key, str(default))
            self.write(open(self.path, 'w'))
            return default

    def setkey(self, key, value):
        self.set(self.s, key, str(value))
        self.write(open(self.path, 'w'))


class MyThread(Thread):
    def __init__(self, target, *args, **kwargs):
        Thread.__init__(self, target=target, args=args, kwargs=kwargs)

        self.result = None
        self.finish = False

        self.start()

    def run(self):
        self.result = self._target(*self._args, **self._kwargs)
        self.finish = True

    def stop(self):
        if not self.finish:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(self.ident, ctypes.py_object(SystemExit))


if __name__ == '__main__':
    import time

    def ThreadFunction(timeout, fun, *args, **kwargs):
        t = MyThread(fun, *args, **kwargs)
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


__all__ = [k for k in globals() if k not in __all__]
