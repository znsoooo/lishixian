"""Decorators"""

import sys
import time
import traceback
from functools import wraps

from .refact import print


__all__ = list(globals())


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


__all__ = [k for k in globals() if k not in __all__]
