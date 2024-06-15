"""Console Scripts"""


def run():
    import re
    import sys
    import inspect

    help = lambda: 'Commands: ' + ' '.join(funcs)

    from . import version
    from . import ip, mac, user
    from . import crc, md5, inv, create, delete, detect
    from . import escape, unescape, quote, unquote
    from . import hex2bin, bin2hex, hex2half, half2hex, hex2float, float2hex, hex2double, double2hex

    funcs = {k: v for k, v in vars().copy().items() if inspect.isfunction(v)}

    funcs['/']    = lambda s: re.sub(r'[\\/]+', r'/', s)
    funcs['\\']   = lambda s: re.sub(r'[\\/]+', r'\\', s)
    funcs['\\\\'] = lambda s: re.sub(r'[\\/]+', r'\\\\', s)

    func = funcs[sys.argv[1]] if len(sys.argv) > 1 else help
    args = sys.argv[2:]

    if args:
        for arg in args:
            print(func(arg) or '')
    else:
        print(func() or '')


if __name__ == '__main__':
    run()
