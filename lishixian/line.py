"""Lambda Functions"""

import os
import re
import json
import uuid
import shutil
import socket
import struct
import getpass
import hashlib
import binascii
import textwrap
from threading import Thread

__all__ = list(globals())

# quick function
fake = lambda *v, **kv: None
pause = lambda: input('Press enter to continue: ')
start = lambda fn, *v, **kv: Thread(target=fn, args=v, kwargs=kv).start()
freeze = lambda fn, *v, **kv: (lambda: fn(*v, **kv))

# file function
crc = lambda b: '0x%04X' % binascii.crc_hqx(b if isinstance(b, bytes) else open(b, 'rb').read(), 0)
md5 = lambda b: hashlib.md5(b if isinstance(b, bytes) else open(b, 'rb').read()).hexdigest()
inv = lambda p: open(p + '.inv', 'wb').write(bytes(255 - b for b in open(p, 'rb').read()))
create = lambda p: os.path.dirname(p) and os.makedirs(os.path.dirname(p), exist_ok=True) or os.path.basename(p) and open(p, 'ab').close()
delete = lambda p: os.remove(p) if os.path.isfile(p) else shutil.rmtree(p) if os.path.isdir(p) else None

# data resort
unique = lambda arr: sorted(set(arr), key=arr.index)
flatten = lambda arr: sum(arr[1:], arr[0])
reshape = lambda arr, width: list(zip(*[iter(arr)]*width))
transpose = lambda arr: list(zip(*arr))

# string function
join = lambda *s, sp='': sp.join(s)
wash = lambda func, arr: [wash(func, v) for v in arr] if isinstance(arr, (list, tuple)) else func(arr)
dumps = lambda data: json.dumps(data, ensure_ascii=False, indent=2)
indent = lambda width, text: textwrap.indent(textwrap.dedent(text)[1:-1], ' ' * width)
str2dict = lambda s: dict(re.findall(r'(.*?):\s*(.*)', s))

# sorting
sort_kv  = lambda d, reverse=False: sorted(d.items(), key=lambda item: item[1], reverse=reverse)
sort_key = lambda d, reverse=False: sorted(d, key=d.__getitem__, reverse=reverse)
sort_num = lambda s: [(s, int(n)) for s, n in re.findall(r'(\D+)(\d+)', 'a%s0' % s)]

# number convert
hex2bin = lambda s: bin(int(s, 16))[2:].zfill(len(s) * 4)
bin2hex = lambda s: hex(int(s, 2))[2:].zfill(len(s) // 4)
half2hex = lambda n: struct.pack('>e', n).hex()
hex2half = lambda s: struct.unpack('>e', bytes.fromhex(s))[0]
float2hex = lambda n: struct.pack('>f', n).hex()
hex2float = lambda s: struct.unpack('>f', bytes.fromhex(s))[0]
double2hex = lambda n: struct.pack('>d', n).hex()
hex2double = lambda s: struct.unpack('>d', bytes.fromhex(s))[0]

# pc tools
ip = lambda: socket.gethostbyname(socket.gethostname())
mac = lambda: '-'.join(re.findall('..', uuid.uuid1().hex[-12:].upper()))
user = lambda: getpass.getuser()

# others
tuple2item = lambda item: item if len(item) > 1 else item[0]


__all__ = [k for k in globals() if k not in __all__]
