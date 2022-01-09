_help = help
_print = print

__keep__ = list(globals()) # Don't use word `__all__`, its will rewrite many times below.


from .cls import *
from .line import *
from .refact import *
from .useful import *
from .decorator import *

try:
    from .np import *
    from .doc import *
    from .gui import *
    from .auto import *
except ImportError as e:
    _print(e)


def help():
    for k in __all__:
        if not k.startswith('_'):
            _help(k)


# __all__ = [k for k in globals() if k not in __keep__]
__all__ = [k for k, v in globals().items() if k not in __keep__ and callable(v)]

_print('functions:', len(__all__))
