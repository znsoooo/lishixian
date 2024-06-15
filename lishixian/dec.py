"""Decorators"""

import sys
import time
import traceback
from functools import wraps
from threading import Thread


__all__ = list(globals())


def main(fn):
    import inspect
    import traceback
    if '__main__' == inspect.currentframe().f_back.f_globals['__name__']:
        try:
            for arg in sys.argv[1:] or [None]:
                try:
                    fn() if arg is None else fn(arg)
                except Exception:
                    traceback.print_exc()
        except KeyboardInterrupt:
            traceback.print_exc()
        input('Press enter to exit: ')
    return fn


def fn2parser(fn):
    import inspect
    import argparse
    if '__main__' != inspect.currentframe().f_back.f_globals['__name__']:
        return fn
    varnames = fn.__code__.co_varnames
    defaults = fn.__defaults__ or ()
    nargs = len(varnames) - len(defaults)
    parser = argparse.ArgumentParser(description=fn.__doc__)
    for i, varname in enumerate(varnames):
        help = None if i < nargs else 'default: ' + repr(defaults[i-nargs])
        parser.add_argument(nargs='?',      dest='pos_' + varname, help=help, metavar=varname)
        parser.add_argument('--' + varname, dest='key_' + varname, help=help, metavar=varname.upper())
    opt = parser.parse_args()
    args = [eval(v) for k, v in vars(opt).items() if k.startswith('p') and v is not None]
    kwargs = {k[4:]: eval(v) for k, v in vars(opt).items() if k.startswith('k') and v is not None}
    fn(*args, **kwargs)
    return fn


def fn2input(fn):
    import inspect
    if '__main__' != inspect.currentframe().f_back.f_globals['__name__']:
        return fn
    varnames = fn.__code__.co_varnames
    defaults = fn.__defaults__ or ()
    nargs = len(varnames) - len(defaults)
    print(fn.__code__.co_name + '(', end='\n' if varnames else '')
    args = [eval(input('  %s = ' % k)) for k in varnames[:nargs]]
    kwargs = {k: eval(input('  %s = %s or ' % (k, repr(v))) or 'v') for k, v in zip(varnames[nargs:], defaults)}
    print(')\n')
    fn(*args, **kwargs)
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
        except Exception:
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
                except Exception:
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
