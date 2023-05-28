# top module functions
all = help = None

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

    module_names = {}
    for module_name, module in globals().items():
        if inspect.ismodule(module) and module.__name__.count('.') == 1:
            for name in module.__all__:
                if not name.startswith('_'):
                    if name not in module_names:
                        module_names[name] = module_name
                    else:
                        print("Warning: '%s.%s' exist in '%s.%s'" % (module_name, name, module_names[name], name), file=sys.stderr)

    for fun in globals().values():
        if inspect.isfunction(fun):
            if fun.__name__ == '<lambda>':
                for k, v in inspect.currentframe().f_back.f_locals.items():
                    if v is fun:
                        fun.__name__ = k
            fun.__qualname__ = fun.__module__ + '.' + fun.__name__

    return ['all', 'help'] + list(module_names)


def help():
    import inspect
    n1 = n2 = 0
    print("# Help on lishixian library")
    print("\n## Top module")
    for k, v in globals().items():
        if not k.startswith('_'):
            if inspect.ismodule(v):
                n1 += 1
                print("\n## Module '%s'" % k)
            else:
                n2 += 1
                try:
                    argspec = str(inspect.signature(v))
                    print("- %s%s" % (k, argspec))
                except (TypeError, ValueError) as e:
                    print("- %s = %r" % (k, v))
    print("\nLibrary lishixian-%s contain %d modules and %d functions." % (__version__, n1, n2))


__all__ = all()
