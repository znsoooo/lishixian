"""Console Scripts"""


def run():
    import os
    import sys
    import inspect

    import html
    import urllib.parse
    from . import __version__

    pkg = __import__

    help = lambda: 'Commands: ' + ' '.join(funcs)
    version = lambda: '%s %s from "%s" (python %d.%d.%d)' % ((__package__, __version__, os.path.dirname(__file__)) + sys.version_info[:3])

    ip = lambda: pkg('socket').gethostbyname(pkg('socket').gethostname())
    mac = lambda: '-'.join(pkg('re').findall('..', pkg('uuid').uuid1().hex[-12:].upper()))
    user = lambda: pkg('getpass').getuser()

    crc = lambda p: '0x%04X' % pkg('binascii').crc_hqx(open(p, 'rb').read(), 0)
    md5 = lambda p: pkg('hashlib').md5(open(p, 'rb').read()).hexdigest()
    inv = lambda p: open(p + '.inv', 'wb').write(bytes(255 - b for b in open(p, 'rb').read()))
    create = lambda p: os.path.dirname(p) and os.makedirs(os.path.dirname(p), exist_ok=True) or os.path.basename(p) and open(p, 'ab').close()
    delete = lambda p: os.remove(p) if os.path.isfile(p) else pkg('shutil').rmtree(p) if os.path.isdir(p) else None
    detect = lambda p: pkg('chardet').detect(open(p, 'rb').read())['encoding'] or 'utf-8'

    hex2bin = lambda hex: bin(int(hex, 16))[2:].zfill(len(hex) * 4)
    bin2hex = lambda bin: hex(int(bin, 2))[2:].zfill(len(bin) // 4)
    half2hex = lambda num: pkg('struct').pack('>e', float(num)).hex()
    hex2half = lambda hex: pkg('struct').unpack('>e', bytes.fromhex(hex))[0]
    float2hex = lambda num: pkg('struct').pack('>f', float(num)).hex()
    hex2float = lambda hex: pkg('struct').unpack('>f', bytes.fromhex(hex))[0]
    double2hex = lambda num: pkg('struct').pack('>d', float(num)).hex()
    hex2double = lambda hex: pkg('struct').unpack('>d', bytes.fromhex(hex))[0]

    escape = html.escape
    unescape = html.unescape
    quote = urllib.parse.quote_plus
    unquote = urllib.parse.unquote

    funcs = {k: v for k, v in vars().copy().items() if inspect.isfunction(v)}

    funcs['/']    = lambda s: pkg('re').sub(r'[\\/]+', r'/', s)
    funcs['\\']   = lambda s: pkg('re').sub(r'[\\/]+', r'\\', s)
    funcs['\\\\'] = lambda s: pkg('re').sub(r'[\\/]+', r'\\\\', s)

    func = funcs[sys.argv[1]] if len(sys.argv) > 1 else help
    args = sys.argv[2:]

    if args:
        for arg in args:
            print(func(arg) or '')
    else:
        print(func() or '')


if __name__ == '__main__':
    run()
