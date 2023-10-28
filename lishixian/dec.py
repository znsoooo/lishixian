"""Decorators"""

import sys
import time
import traceback
from functools import wraps
from threading import Thread


__all__ = list(globals())


def main(f):
    import inspect
    if '__main__' == inspect.currentframe().f_back.f_globals['__name__']:
        try:
            if len(sys.argv) == 1:
                f()
            for v in sys.argv[1:]:
                f(v)
        except Exception:
            import traceback
            traceback.print_exc()
        input('Press enter to exit: ')
    return f


def parser(f):
    import inspect
    import argparse
    if '__main__' == inspect.currentframe().f_back.f_globals['__name__']:
        def convert(var):
            try:
                return eval(var)
            except Exception:
                return var
        varnames = f.__code__.co_varnames
        defaults = f.__defaults__
        defaults = (None,) * (len(varnames) - len(defaults)) + defaults
        parser = argparse.ArgumentParser()
        for varname, default in zip(varnames, defaults):
            parser.add_argument('--' + varname, default=default)
        opt = parser.parse_args()
        kwargs = {k: convert(v) for k, v in vars(opt).items()}
        f(**kwargs)
    return f


def timeit(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        s = time.time()
        ret = f(*args, **kwargs)
        e = time.time()
        print('Running <%s>: %.4f' % (f.__name__, e - s))
        return ret
    return wrapper


def tracer(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        print('Enter function:', f.__name__)
        if args:
            print('args:', args)
        if kwargs:
            print('kwargs:', kwargs)
        s = time.time()
        ret = f(*args, **kwargs)
        e = time.time()
        print('Leave function:', e - s)
        return ret
    return wrapper


def protect(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            msg = traceback.format_exc()
            print(msg, file=sys.stderr)
            return msg
    return wrapper


def surround(before=(), after=()):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # print(func.__name__) # for test
            [f() for f in before]
            ret = func(*args, **kwargs)
            [f() for f in after]
            return ret
        return wrapper
    return decorator


def hotkey(key='F12'):
    key = key.lower()
    def decorator(f):
        def press(key2):
            if key == str(key2).split('.')[-1].lower():
                f()
        def th():
            import pynput
            with pynput.keyboard.Listener(press) as kl:
                kl.join()
        Thread(target=th).start()
        return f
    return decorator


def threads(cnt):
    import threading
    counter = threading.BoundedSemaphore(cnt)
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            def th():
                try:
                    f(*args, **kwargs)
                except:
                    raise
                finally:
                    counter.release()
            counter.acquire()
            threading.Thread(target=th).start()
        return wrapper
    return decorator


__all__ = [k for k in globals() if k not in __all__]


if __name__ == '__main__':
    import random

    @threads(10)
    def delay():
        t = 1 + random.random() / 5
        assert t < 1.19
        time.sleep(t)
        print(t)

    while 1:
        delay()
