"""Lambda Functions"""

import re
import sys
import json
import uuid
import random
import socket
import getpass
import hashlib
from threading import Thread

__all__ = list(globals())

s128 = bytes(range(128)).decode()
s127 = bytes(range(32, 127)).decode()

empty = lambda *v, **kv: None

t = lambda arr: list(zip(*arr))

md5 = lambda b: hashlib.md5(b).hexdigest()
start = lambda func, *args, **kwargs: Thread(target=func, args=args, kwargs=kwargs).start()
create = lambda file: open(file).close()
pprint = lambda *value, file=sys.stdout: print(' '.join(map(str, value)) + '\n', end='', file=file)

dumps = lambda data: json.dumps(data, ensure_ascii=False, indent=2)

sort_kv  = lambda d, reverse=False: sorted(d.items(), key=lambda item: item[1], reverse=reverse)
sort_key = lambda d, reverse=False: sorted(d, key=d.__getitem__, reverse=reverse)
sort_num = lambda s: [(s, int(n)) for s, n in re.findall(r'(\D+)(\d+)', 'a%s0' % s)]

raw2headers = str2dict = lambda s: dict(re.findall(r'(.*?):(.*)', s))
# Accept: image/gif, image/jpeg, image/pjpeg, */*
# Referer: ****
# Accept-Language: zh-cn
# User-Agent: Mozilla/4.0 ****
# Cookie: ****

# todo 函数重名
unique = lambda arr: sorted(list(set(arr)), key=arr.index)
unique = lambda arr: [item for i, item in enumerate(arr) if arr.index(item) == i]

pc_ip = lambda: socket.gethostbyname(socket.gethostname())
pc_mac = lambda: '-'.join(re.findall('..', uuid.uuid1().hex[-12:].upper()))
pc_user = lambda: getpass.getuser()

randombytes = lambda n: bytes(random.randint(0, 255) for i in range(n))

# def pc_ip():
#     for addr in os.popen('route print').readlines():
#         if '0.0.0.0' in addr:
#             return addr.split()[-2]

tuple2item = lambda item: item if len(item) > 1 else item[0]

join = lambda *s, sp='': sp.join(s)


__all__ = [k for k in globals() if k not in __all__]
