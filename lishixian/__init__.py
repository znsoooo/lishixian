"""
Lite Software eXtension

Usage:
    import lishixian as lsx
    lsx.help()

License:
    MIT license.
    Copyright (c) 2021-2024 Shixian Li (znsoooo). All rights reserved.
"""

# top module functions
all = help = version = None

# base on built-in library
from .new import *
from .line import *
from .util import *
from .dec import *
from .cls import *

# only work on windows platform
if __import__('platform').system() == 'Windows':
    from .reg import *
    from .windll import *

# 3rd-library needed
from .doc import *
from .np import *
from .auto import *
from .gui import *


__author__  = 'Shixian Li <lsx7@sina.com>'
__credits__ = 'https://github.com/znsoooo/lishixian'
__date__    = '2024'
from .version import __version__


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


def version():
    import os
    import sys
    return '%s %s from "%s" (python %d.%d.%d)' % ((__package__, __version__, os.path.dirname(__file__)) + sys.version_info[:3])


__all__ = all()
