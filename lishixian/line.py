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
crc = lambda path: '0x%04X' % binascii.crc_hqx(path if isinstance(path, bytes) else open(path, 'rb').read(), 0)
md5 = lambda path: hashlib.md5(path if isinstance(path, bytes) else open(path, 'rb').read()).hexdigest()
inv = lambda path: open(path + '.inv', 'wb').write(bytes(255 - b for b in open(path, 'rb').read()))
create = lambda path: os.path.dirname(path) and os.makedirs(os.path.dirname(path), exist_ok=True) or os.path.basename(path) and open(path, 'ab').close()
delete = lambda path: os.remove(path) if os.path.isfile(path) else shutil.rmtree(path) if os.path.isdir(path) else None

# data resort
unique = lambda arr: sorted(set(arr), key=arr.index)
flatten = lambda arr: sum(arr[1:], arr[0])
reshape = lambda arr, width: list(zip(*[iter(arr)]*width))
transpose = lambda arr: list(zip(*arr))

# string function
join = lambda *string, sep='': sep.join(string)
wash = lambda func, arr: [wash(func, v) for v in arr] if isinstance(arr, (list, tuple)) else func(arr)
dumps = lambda data: json.dumps(data, ensure_ascii=False, indent=2)
indent = lambda width, text: textwrap.indent(textwrap.dedent(text)[1:-1], ' ' * width)
str2dict = lambda text: dict(re.findall(r'(.*?):\s*(.*)', text))

# sorting
sort_kv  = lambda dic, reverse=False: sorted(dic.items(), key=lambda item: item[1], reverse=reverse)
sort_key = lambda dic, reverse=False: sorted(dic, key=dic.__getitem__, reverse=reverse)
sort_num = lambda text: [(s, int(n)) for s, n in re.findall(r'(\D+)(\d+)', 'a%s0' % text)]

# number convert
hex2bin = lambda hex: bin(int(hex, 16))[2:].zfill(len(hex) * 4)
bin2hex = lambda bin: hex(int(bin, 2))[2:].zfill(len(bin) // 4)
half2hex = lambda num: struct.pack('>e', num).hex()
hex2half = lambda hex: struct.unpack('>e', bytes.fromhex(hex))[0]
float2hex = lambda num: struct.pack('>f', num).hex()
hex2float = lambda hex: struct.unpack('>f', bytes.fromhex(hex))[0]
double2hex = lambda num: struct.pack('>d', num).hex()
hex2double = lambda hex: struct.unpack('>d', bytes.fromhex(hex))[0]

# pc tools
ip = lambda: socket.gethostbyname(socket.gethostname())
mac = lambda: '-'.join(re.findall('..', uuid.uuid1().hex[-12:].upper()))
user = lambda: getpass.getuser()

# others
tuple2item = lambda item: item if len(item) > 1 else item[0]


__all__ = [k for k in globals() if k not in __all__]
