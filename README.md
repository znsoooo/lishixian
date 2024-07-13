# Lite Software eXtension

Contain 11 modules and 163 functions.


## About

- __Author:__ Lishixian
- __QQ:__ 11313213
- __Email:__ lsx7@sina.com
- __Github:__ https://github.com/znsoooo/lishixian
- __License:__ MIT License. Copyright (c) 2021-2024 Shixian Li (znsoooo). All rights reserved.


## Install

Install on pip:

```bash
pip install lishixian --upgrade
```

Install on Github:

```bash
git clone https://github.com/znsoooo/lishixian
cd lishixian
pip install .
```


## Usage

Use it in Python script:

```python
import lishixian as lsx
lsx.help()
```

The package can also be used in console, it takes one or zero parameter:

```bash
$ lishixian help
Commands: help version ip mac user crc md5 inv create delete detect escape unescape quote unquote hex2bin bin2hex hex2half half2hex hex2float float2hex hex2double double2hex / \ \\

$ lishixian float2hex 1.0
3f800000
```

## Modules

### Top module
- all()
- help()
- version()

### Module 'new'
- print(*value, file=True)
- loop(start=0, step=1)
- randbytes(n)
- breakpoint()
- popen(cmd, encoding=None)
- listdir(*paths)
- findall(pattern, string, flags=0)
- split(arr, cols)
- sum(seq)
- pack(fmt, values)
- unpack(fmt, string)
- system(cmd, encoding=None)
- detect(path)
- walk(paths='.', exts='')
- bytes(data, width=16)
- memoryview(data, width=16, offset=0)

### Module 'line'
- fake(*v, **kv)
- pause()
- start(fn, *v, **kv)
- freeze(fn, *v, **kv)
- crc(path)
- md5(path)
- inv(path)
- create(path)
- delete(path)
- unique(arr)
- flatten(arr)
- reshape(arr, width)
- transpose(arr)
- join(*string, sep='')
- wash(func, arr)
- dumps(data)
- indent(width, text)
- str2dict(text)
- time(sep='')
- date(sep='')
- stamp(fmt)
- sort_kv(dic, reverse=False)
- sort_key(dic, reverse=False)
- sort_num(text)
- hex2bin(hex)
- bin2hex(bin)
- half2hex(num)
- hex2half(hex)
- float2hex(num)
- hex2float(hex)
- double2hex(num)
- hex2double(hex)
- ip()
- mac()
- user()
- tuple2item(item)

### Module 'util'
- log(*value, file='log.txt')
- redirect(file='log.txt', prefix='[%Y-%m-%d %H:%M:%S]')
- sudo()
- kill(ths=None)
- check(obj, patt='.*', stdout=True)
- print_paths()
- print_lines(lines)
- print_table(table)
- progress(*value, interval=1)
- fps()
- count(add=1, name='default')
- recent(iterable, max=0)
- parser2opt(parser, opt='opt')
- p1 = dirname(path, new='')
- p2 = stem(path)
- p3 = ext(path)
- p12 = root(path, new='')
- p23 = basename(path, new='')
- p123(path, new='')
- select(p)
- file_mtime(path)
- file_ctime(path)
- file_utime(path, date)
- path_mark(path, mark='.bak')
- path_safe(path, repl=None)
- path_split(path)
- path_unique(path, dash='-', start=2)
- copy(src, dst, overwrite=True)
- move(src, dst, overwrite=True)
- factorize(num)
- primes(max)
- escape(s, quote=True)
- unescape(s)
- quote(string, safe='', encoding=None, errors=None)
- unquote(string, encoding='utf-8', errors='replace')
- b64encode(s)
- b64decode(s)
- urlopen(url, base='', query=None, fragment=None, data=None, headers=None, method=None, retry=1, timeout=10, strict=True)
- scan(format, string)
- findpair(text, pair='()', start=0)
- install(path)
- input_wait(msg)
- input_default(msg, default)
- Catch()
- catch = \<Catch object\>

### Module 'dec'
- main(fn)
- fn2parser(fn)
- fn2input(fn)
- timeit(fn)
- tracer(fn)
- protect(fn)
- surround(before=(), after=())
- hotkey(key='F12')
- threads(cnt)

### Module 'cls'
- Config(path, section='default', encoding='u8')
- Thread(target, *args, **kwargs)
- Tcp(addr, port)
- Udp(addr, port)

### Module 'reg'
- GetDir(name, local=False)
- DeleteRecu(key)
- DeleteKey(key, name='')
- SetKey(key, name='', val='')
- NewFilePy()

### Module 'windll'
- MessageBox(info, title='Message', style=0)
- DirDialog(message=None)
- OpenFileDialog(title=None, filter='', path='')
- SaveFileDialog(title=None, filter='', path='')

### Module 'doc'
- readb(path)
- read(path, encoding='u8', strict=True)
- write(path, data='', encoding='u8')
- ReadIni(path, encoding='u8')
- WriteIni(path, dic, encoding='u8')
- ReadTxt(path, encoding='u8', sep=None)
- WriteTxt(path, data, encoding='u8', sep=' ')
- ReadCsv(path, encoding='utf-8-sig')
- WriteCsv(path, data, encoding='utf-8-sig', errors='ignore')
- WriteExcel(path, data, new_sheet='sheet1')
- OpenExcel(path)
- MergeCell(data, merge, merge_x=True, merge_y=True, strip_x=False)
- ReadExcel(path, merge_x=True, merge_y=True, strip_x=False)
- ReadSheet(path, index=0)
- Doc2Docx(path, overwrite=False)
- OpenDocx(path)
- ReadWordTexts(path)
- ReadWord(path, merge_x=True, merge_y=True, strip_x=False)
- ReadFile(path, merge_x=True, merge_y=True, strip_x=False)
- File2Csv(path, merge_x=True, merge_y=True, strip_x=False)
- ReadFiles(paths, merge_x=True, merge_y=True, strip_x=False)

### Module 'np'
- imread(path)
- imwrite(path, img)
- imshow(img, delay=50, title='')
- imsave(path)
- imiter(file_or_id)

### Module 'auto'
- shortcut(p=None, make=True)
- paste(word, tab=0)
- Monitor(func)
- Recoder(complete=False)

### Module 'gui'
- center(top)
- WrapBox(parent, w, label='')
- GetClipboard()
- SetClipboard(text)
- Mover(parent, widget)
- EventThread(parent, id, target=bool, *args, **kwargs)


## Extra

- Library [lsx](https://pypi.org/project/lsx) is as same as [lishixian](https://pypi.org/project/lishixian) in [pypi.org](https://pypi.org).
