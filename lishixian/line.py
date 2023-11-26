"""Lambda Functions"""

import re
import sys
import json
import uuid
import socket
import struct
import getpass
import hashlib
import binascii
from threading import Thread

__all__ = list(globals())

# quick function
fake = lambda *v, **kv: None
start = lambda fn, *v, **kv: Thread(target=fn, args=v, kwargs=kv).start()
freeze = lambda fn, *v, **kv: (lambda: fn(*v, **kv))
pprint = lambda *value, file=sys.stdout: print(' '.join(map(str, value)) + '\n', end='', file=file)

# file function
crc = lambda b: '0x%04X' % binascii.crc_hqx(b if isinstance(b, bytes) else open(b, 'rb').read(), 0)
md5 = lambda b: hashlib.md5(b if isinstance(b, bytes) else open(b, 'rb').read()).hexdigest()
inv = lambda p: open(p + '.inv', 'wb').write(bytes(255 - b for b in open(p, 'rb').read()))
create = lambda file: open(file, 'w').close()

# data resort
unique = lambda arr: sorted(set(arr), key=arr.index)
flatten = lambda arr: sum(arr[1:], arr[0])
reshape = lambda arr, width: list(zip(*[iter(arr)]*width))
transpose = lambda arr: list(zip(*arr))

# string function
join = lambda *s, sp='': sp.join(s)
dumps = lambda data: json.dumps(data, ensure_ascii=False, indent=2)
str2dict = lambda s: dict(re.findall(r'(.*?):(.*)', s))

# sorting
sort_kv  = lambda d, reverse=False: sorted(d.items(), key=lambda item: item[1], reverse=reverse)
sort_key = lambda d, reverse=False: sorted(d, key=d.__getitem__, reverse=reverse)
sort_num = lambda s: [(s, int(n)) for s, n in re.findall(r'(\D+)(\d+)', 'a%s0' % s)]

# number convert
num2hex = lambda n, fmt='>d': struct.pack(fmt, n).hex()
hex2num = lambda s, fmt='>d': struct.unpack(fmt, bytes.fromhex(s))[0]
hex2bin = lambda s: bin(int(s, 16))[2:].zfill(len(s) * 4)
bin2hex = lambda s: hex(int(s, 2))[2:].zfill(len(s) // 4)

# pc tools
pc_ip = lambda: socket.gethostbyname(socket.gethostname())
pc_mac = lambda: '-'.join(re.findall('..', uuid.uuid1().hex[-12:].upper()))
pc_user = lambda: getpass.getuser()

# others
tuple2item = lambda item: item if len(item) > 1 else item[0]


__all__ = [k for k in globals() if k not in __all__]
