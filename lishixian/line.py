import re
import sys
import json
import hashlib
from threading import Thread

__except = list(vars())

md5 = lambda b: hashlib.md5(b).hexdigest()
start = lambda func, *args, **kwargs: Thread(target=func, args=args, kwargs=kwargs).start()
# pprint = lambda *value, file=sys.stdout: print(' '.join(map(str, value)) + '\n', end='', file=file)
create = lambda file: open(file).close()

dumps = lambda data: json.dumps(data, ensure_ascii=False, indent=2)

sort_key = lambda d, reverse=False: sorted(d.items(), key=lambda item: item[1], reverse=reverse)
sort_num = lambda s: [(s, int(n)) for s, n in re.findall(r'(\D+)(\d+)', 'a%s0' % s)]

raw2headers = str2dict = lambda s: dict(re.findall(r'(.*?):(.*)', s))
# Accept: image/gif, image/jpeg, image/pjpeg, */*
# Referer: ****
# Accept-Language: zh-cn
# User-Agent: Mozilla/4.0 ****
# Cookie: ****

__all__ = [k for k in vars() if k not in __except]
