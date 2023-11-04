def run():
    import sys
    import inspect

    import html
    import urllib.parse
    from . import __version__

    pkg = __import__

    help = lambda: 'Commands: ' + ' '.join(reversed(funcs))
    version = lambda: __version__

    ip = lambda: pkg('socket').gethostbyname(pkg('socket').gethostname())
    mac = lambda: '-'.join(pkg('re').findall('..', pkg('uuid').uuid1().hex[-12:].upper()))
    user = lambda: pkg('getpass').getuser()

    crc = lambda p: '0x%04X' % pkg('binascii').crc_hqx(open(p, 'rb').read(), 0)
    md5 = lambda p: pkg('hashlib').md5(open(p, 'rb').read()).hexdigest()
    inv = lambda p: open(p + '.inv', 'wb').write(bytes(255 - b for b in open(p, 'rb').read()))
    create = lambda p: open(p, 'w').close()
    detect = lambda p: pkg('chardet').detect(open(p, 'rb').read())['encoding'] or 'utf-8'

    float2hex = lambda num: pkg('struct').pack('>f', float(num)).hex()
    hex2float = lambda hex: pkg('struct').unpack('>f', bytes.fromhex(hex))[0]
    double2hex = lambda num: pkg('struct').pack('>d', float(num)).hex()
    hex2double = lambda hex: pkg('struct').unpack('>d', bytes.fromhex(hex))[0]

    escape = html.escape
    unescape = html.unescape
    quote = urllib.parse.quote_plus
    unquote = urllib.parse.unquote

    funcs = [k for k, v in vars().copy().items() if inspect.isfunction(v)]

    if len(sys.argv) == 1:
        sys.argv.append('help')
    name, *args = sys.argv[1:]
    print(vars()[name](*args))


if __name__ == '__main__':
    run()
