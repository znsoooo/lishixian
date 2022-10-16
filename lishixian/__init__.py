# base on built-in library
from .cls import *
from .dec import *
from .new import *
from .line import *
from .useful import *
from .windll import *

# 3rd-library needed
from .auto import *
from .doc import *
from .gui import *
from .np import *


def all():
    import sys
    import inspect
    table = {}
    for module, obj in globals().items():
        if inspect.ismodule(obj) and obj.__name__.count('.') == 1:
            for name in obj.__all__:
                if name not in table:
                    table[name] = module
                elif name != '__all__':
                    print("Warnning: '%s.%s' exist in '%s.%s'" % (module, name, table[name], name), file=sys.stderr)
    return list(table) + ['all', 'help']


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


__all__ = all()
