# Lishixian Library
Contain 111 functions.


## About
- __Author:__ Lishixian
- __QQ:__ 11313213
- __Email:__ lsx7@sina.com
- __Github:__ https://github.com/znsoooo/lishixian
- __License:__ MIT License. Copyright (c) 2022 Lishixian (znsoooo). All Rights Reserved.


## Install
```bash
pip install lishixian --upgrade
```


## Modules

### Top module
- all()
- help()

### Module 'cls'
- Config(path, section='default', encoding='u8')
- Thread(target, *args, **kwargs)
- Tcp(addr, port)

### Module 'dec'
- main(f)
- timeit(f)
- tracer(f)
- protect(f)
- surround(before=(), after=())
- hotkey(key='F12')
- threads(cnt)

### Module 'new'
- print(*value, file=sys.stdout)
- infinity = <class 'itertools.count'>
- makedirs(name, mode=511, *, exist_ok=True)
- breakpoint()
- popen(cmd)
- listdir(*paths)
- findall(pattern, string, flags=0)
- split(arr, cols)
- detect(file)
- walk(paths, exts='')
- open(file)

### Module 'line'
- s128 = bytes(range(128)).decode()
- s127 = bytes(range(32, 127)).decode()
- empty(*v, **kv)
- freeze(fn, *v, **kv)
- t(arr)
- md5(b)
- mask(p)
- start(func, *args, **kwargs)
- create(file)
- pprint(*value, file=sys.stdout)
- dumps(data)
- sort_kv(d, reverse=False)
- sort_key(d, reverse=False)
- sort_num(s)
- str2dict(s)
- tuple2item(item)
- unique(arr)
- pc_ip()
- pc_mac()
- pc_user()
- randombytes(n)
- join(*s, sp='')

### Module 'useful'
- tag()
- log(*value)
- check(obj, patt='.*')
- fps()
- select(path)
- path_mark(path, mark='.bak')
- path_quote(p, repl=None)
- path_split(p)
- path_unique(p, dash='-')
- escape(s, quote=True)
- unescape(s)
- quote(string, safe='', encoding=None, errors=None)
- unquote(string, encoding='utf-8', errors='replace')
- urlopen(url, timeout=5)
- findpair(s, p1='(', p2=')', st=0)
- bytes_format(data, n=16)
- bytes_print(data, n=16)
- bytes_hex(data, offset=0, length=-1, slice=-1)
- install(path, block=False)
- input_wait(msg)
- input_default(msg, default)
- Catch(log='log.txt')
- catch = <Catch object>

### Module 'windll'
- MessageBox(info, title='Message', style=0)
- DirDialog(message=None)
- OpenFileDialog(title=None, filter='', path='')
- SaveFileDialog(title=None, filter='', path='')

### Module 'auto'
- shortcut(p=None, make=True)
- copy(word, tab=0)
- Monitor(func)
- Recoder(complete=False)

### Module 'doc'
- read(file)
- write(file, data)
- ReadIni(file, encoding='u8')
- WriteIni(file, dic, encoding='u8')
- WriteTxt(file, data, encoding='utf-8-sig')
- ReadCsv(file, encoding='utf-8-sig')
- WriteCsv(file, data, encoding='utf-8-sig', errors='ignore')
- WriteExcel(file, data, new_sheet='sheet1')
- OpenExcel(file)
- MergeCell(data, merge, merge_x=True, merge_y=True, strip_x=False)
- ReadExcel(file, merge_x=True, merge_y=True, strip_x=False)
- ReadSheet(file, index=0)
- Doc2Docx(file, overwrite=False)
- OpenDocx(file)
- ReadWordTexts(file)
- ReadWord(file, merge_x=True, merge_y=True, strip_x=False)
- ReadFile(file, merge_x=True, merge_y=True, strip_x=False)
- File2Csv(file, merge_x=True, merge_y=True, strip_x=False)
- ReadFiles(files, merge_x=True, merge_y=True, strip_x=False)

### Module 'gui'
- center(top)
- WrapBox(parent, w, label='')
- GetClipboard()
- SetClipboard(text)
- Mover(parent, widget)
- EventThread(parent, id, target=<class 'bool'>, *args, **kwargs)

### Module 'np'
- imread(file)
- imwrite(file, im)
- imshow(img, delay=50, title='')
- imsave(file)
- imiter(file_or_id, st=None, ed=None)


## Comment
1. Lib `lsx` is same as `lishixian` in `pypi.org`.
2. If you **really** need domain `lsx` in `pypi.org`, contact me with `Email`.
