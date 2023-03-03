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
                if name not in module_names:
                    module_names[name] = module_name
                elif name != '__all__':
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
