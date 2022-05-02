_help = help
_print = print

__keep__ = list(globals()) # Don't use word `__all__`, its will rewrite many times below.


def help():
    import inspect
    import importlib
    print("\n# Lishixian Library")
    print("Contain %d functions." % len(__all__))
    print("\n## Top module")
    for k, v in globals().items():
        if not k.startswith('_'):
            if inspect.ismodule(v):
                print("\n## Module '%s'" % k)
            else:
                try:
                    argspec = str(inspect.signature(v))
                    print("- %s%s" % (k, argspec))
                except (TypeError, ValueError) as e:
                    print("- %s = %r" % (k, v))


# base on built-in library
from .cls import *
from .decorator import *
from .line import *
from .refact import *
from .useful import *
from .windll import *

# 3rd-library needed
from .auto import *
from .doc import *
from .gui import *
from .np import *

# __all__ = [k for k in globals() if k not in __keep__]
__all__ = [k for k, v in globals().items() if k not in __keep__ and callable(v)]
