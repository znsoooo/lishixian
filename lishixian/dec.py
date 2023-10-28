"""Decorators"""

import sys
import time
import traceback
from functools import wraps
from threading import Thread


__all__ = list(globals())


def main(fn):
    import inspect
    if '__main__' == inspect.currentframe().f_back.f_globals['__name__']:
        try:
            if len(sys.argv) == 1:
                fn()
            for v in sys.argv[1:]:
                fn(v)
        except Exception:
            import traceback
            traceback.print_exc()
        input('Press enter to exit: ')
    return fn


def parser(fn):
    import inspect
    import argparse
    if '__main__' == inspect.currentframe().f_back.f_globals['__name__']:
        def convert(var):
            try:
                return eval(var)
            except Exception:
                return var
        varnames = fn.__code__.co_varnames
        defaults = fn.__defaults__
        defaults = (None,) * (len(varnames) - len(defaults)) + defaults
        parser = argparse.ArgumentParser()
        for varname, default in zip(varnames, defaults):
            parser.add_argument('--' + varname, default=default)
        opt = parser.parse_args()
        kwargs = {k: convert(v) for k, v in vars(opt).items()}
        fn(**kwargs)
    return fn


def timeit(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        s = time.time()
        ret = fn(*args, **kwargs)
        e = time.time()
        print('Running <%s>: %.4f' % (fn.__name__, e - s))
        return ret
    return wrapper


def tracer(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print('Enter function:', fn.__name__)
        if args:
            print('args:', args)
        if kwargs:
            print('kwargs:', kwargs)
        s = time.time()
        ret = fn(*args, **kwargs)
        e = time.time()
        print('Leave function:', e - s)
        return ret
    return wrapper


def protect(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            msg = traceback.format_exc()
            print(msg, file=sys.stderr)
            return msg
    return wrapper


def surround(before=(), after=()):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # print(func.__name__) # for test
            [f() for f in before]
            ret = fn(*args, **kwargs)
            [f() for f in after]
            return ret
        return wrapper
    return decorator


def hotkey(key='F12'):
    key = key.lower()
    def decorator(fn):
        def press(key2):
            if key == str(key2).split('.')[-1].lower():
                fn()
        def th():
            import pynput
            with pynput.keyboard.Listener(press) as kl:
                kl.join()
        Thread(target=th).start()
        return fn
    return decorator


def threads(cnt):
    import threading
    counter = threading.BoundedSemaphore(cnt)
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            def th():
                try:
                    fn(*args, **kwargs)
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
