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
    spec = inspect.getfullargspec(fn)
    varnames = spec.args + spec.kwonlyargs
    defaults = list(spec.defaults) + [spec.kwonlydefaults[arg] for arg in spec.kwonlyargs]
    nargs = len(varnames) - len(defaults)
    parser = argparse.ArgumentParser(description=fn.__doc__)
    for i, varname in enumerate(varnames):
        help = None if i < nargs else '[default: %r]' % defaults[i-nargs]
        parser.add_argument(nargs='?', dest='pos_' + varname, help=help, metavar=varname)
        parser.add_argument('--' + varname.replace('_', '-'), dest='key_' + varname, help=help, metavar=varname.upper())
    opt = parser.parse_args()
    args = [eval(v) for k, v in vars(opt).items() if k.startswith('p') and v is not None]
    kwargs = {k[4:]: eval(v) for k, v in vars(opt).items() if k.startswith('k') and v is not None}
    fn(*args, **kwargs)
    return fn


def fn2input(fn):
    import inspect
    if '__main__' != inspect.currentframe().f_back.f_globals['__name__']:
        return fn
    spec = inspect.getfullargspec(fn)
    varnames = spec.args + spec.kwonlyargs
    defaults = list(spec.defaults) + [spec.kwonlydefaults[arg] for arg in spec.kwonlyargs]
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
        t1 = time.time()
        ret = fn(*args, **kwargs)
        t2 = time.time()
        print("finished '%s' in %.4fs" % (fn.__name__, t2 - t1))
        return ret
    return wrapper


def trace(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        args_str = ', '.join(repr(arg) for arg in args)
        kwargs_str = ', '.join('%s=%r' % (key, value) for key, value in kwargs.items())
        comma_str = ', ' if args and kwargs else ''
        call_str = '%s(%s%s%s)' % (fn.__name__, args_str, comma_str, kwargs_str)
        print('[ENTER] %s' % call_str)
        t1 = time.time()
        ret = fn(*args, **kwargs)
        t2 = time.time()
        print('[LEAVE] %s = %r @ %.4fs' % (call_str, ret, t2 - t1))
        return ret
    return wrapper


def protect(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception:
            msg = traceback.format_exc()
            print(msg + '\n', file=sys.stderr, end='')
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


def threads(cnt=-1, order=True):
    """
    @threads(8)
    def foo(arg):
        ...

    for i in range(20):
        if ret := foo(i):
            print(ret)
    for ret in foo(...):
        print(ret)

    """

    import threading
    from functools import wraps

    if callable(cnt):  # use @threads directly
        return threads(-1, order)(cnt)

    class Counter:
        def __init__(self, cnt):
            self.counter = threading.BoundedSemaphore(cnt) if cnt >= 0 else None

        def acquire(self):
            self.counter and self.counter.acquire()

        def release(self):
            self.counter and self.counter.release()

    class Task:
        def __init__(self, fn, *args, **kwargs):
            self.fn = fn
            self.args = args
            self.kwargs = kwargs
            self.result = None
            self.finish = False
            threading.Thread(target=self.run).start()

        def run(self):
            try:
                self.result = self.fn(*self.args, **self.kwargs)
            except Exception:
                raise
            finally:
                self.finish = True
                counter.release()

    class Tasks:
        def __init__(self, fn):
            self.fn = fn
            self.tasks = []
            self.pop = self.pop_next if order else self.pop_any

        def run(self, *args, **kwargs):
            if (args, kwargs) == ((...,), {}):
                return self.pop_last()

            counter.acquire()
            task = Task(self.fn, *args, **kwargs)
            self.tasks.append(task)
            return self.pop()

        def pop_any(self):
            for task in self.tasks:
                if task.finish:
                    self.tasks.remove(task)
                    return task.result

        def pop_next(self):
            if self.tasks:
                task = self.tasks[0]
                if task.finish:
                    self.tasks.remove(task)
                return task.result  # TODO: `task.finish` and `task.result` may out of sync

        def pop_last(self):
            while self.tasks:
                result = self.pop()
                if result:
                    yield result

    def decorator(fn):
        run = Tasks(fn).run
        @wraps(fn)
        def wrapper(*args, **kwargs):
            return run(*args, **kwargs)
        return wrapper

    counter = Counter(cnt)
    return decorator


__all__ = [k for k in globals() if k not in __all__]


if __name__ == '__main__':
    @threads(8, order=True)
    def foo(id):
        import time, random
        t = random.randint(1, 10) / 2
        ret = str((id, t))
        print('In: %s\n' % ret, end='')
        time.sleep(t)
        print('Out: %s\n' % ret, end='')
        return ret

    for i in range(50):
        ret = foo(i)
        if ret:
            print('Return: %s\n' % ret, end='')
    for ret in foo(...):
        print('Last return: %s\n' % ret, end='')
