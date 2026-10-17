"""Console Scripts"""


def run():
    import re
    import sys
    import inspect

    help = lambda: 'Commands: ' + ' '.join(funcs)

    from . import version
    from . import ip, ipv6, mac, user
    from . import crc16, crc32, md5, sha1, sha256, checksum, inv, create, delete, detect
    from . import escape, unescape, quote, unquote
    from . import hex2bin, bin2hex, hex2half, half2hex, hex2float, float2hex, hex2double, double2hex

    funcs = {k: v for k, v in vars().copy().items() if inspect.isfunction(v)}

    funcs['/']    = lambda s: re.sub(r'[\\/]+', r'/', s)
    funcs['\\']   = lambda s: re.sub(r'[\\/]+', r'\\', s)
    funcs['\\\\'] = lambda s: re.sub(r'[\\/]+', r'\\\\', s)

    func = funcs[sys.argv[1]] if len(sys.argv) > 1 else help
    show = lambda v: print('\n'.join(v) if isinstance(v, list) else v or '')
    args = sys.argv[2:]

    if args:
        for arg in args:
            show(func(arg))
    else:
        show(func())


if __name__ == '__main__':
    run()
