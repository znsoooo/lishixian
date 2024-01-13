# Lite Software eXtension

Contain 11 modules and 144 functions.


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
pip install -e .
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
Commands: help version ip mac user crc md5 inv create delete detect half2hex hex2half float2hex hex2float double2hex hex2double escape unescape quote unquote

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
- time(start=0)
- loop(start=0, step=1)
- randbytes(n)
- breakpoint()
- popen(cmd)
- listdir(*paths)
- findall(pattern, string, flags=0)
- split(arr, cols)
- pack(fmt, values)
- unpack(fmt, string)
- detect(file)
- walk(paths='.', exts='')
- bytes(data, width=16)
- memoryview(data, width=16, offset=0)

### Module 'line'
- fake(*v, **kv)
- pause()
- start(fn, *v, **kv)
- freeze(fn, *v, **kv)
- crc(b)
- md5(b)
- inv(p)
- create(p)
- delete(p)
- unique(arr)
- flatten(arr)
- reshape(arr, width)
- transpose(arr)
- join(*s, sp='')
- wash(func, arr)
- dumps(data)
- indent(width, text)
- str2dict(s)
- sort_kv(d, reverse=False)
- sort_key(d, reverse=False)
- sort_num(s)
- hex2bin(s)
- bin2hex(s)
- half2hex(n)
- hex2half(s)
- float2hex(n)
- hex2float(s)
- double2hex(n)
- hex2double(s)
- ip()
- mac()
- user()
- tuple2item(item)

### Module 'util'
- log(*value, file='log.txt')
- sudo()
- check(obj, patt='.*', stdout=True)
- print_paths()
- print_lines(lines)
- print_table(table)
- progress(*value, interval=1)
- fps()
- count(value=None, target=None)
- recent(iterable, max=0)
- parser2opt(parser, opt='opt')
- ext(p)
- stem(p)
- select(p)
- file_mtime(p)
- file_ctime(p)
- file_utime(p, date)
- path_mark(p, mark='.bak')
- path_safe(p, repl=None)
- path_split(p)
- path_unique(p, dash='-', start=2)
- factorize(num)
- primes(max)
- escape(s, quote=True)
- unescape(s)
- quote(string, safe='', encoding=None, errors=None)
- unquote(string, encoding='utf-8', errors='replace')
- urlopen(url, base='', data=None, headers={}, method=None, timeout=10)
- scan(format, string)
- findpair(s, p1='(', p2=')', st=0)
- install(path)
- input_wait(msg)
- input_default(msg, default)
- Catch(log='log.txt')
- catch = <Catch object>

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
- readb(p)
- read(file, encoding='u8')
- write(file, data, encoding='u8')
- ReadIni(file, encoding='u8')
- WriteIni(file, dic, encoding='u8')
- ReadTxt(file, encoding='u8', sep=None)
- WriteTxt(file, data, encoding='u8', sep=' ')
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

### Module 'np'
- imread(file)
- imwrite(file, im)
- imshow(img, delay=50, title='')
- imsave(file)
- imiter(file_or_id)

### Module 'auto'
- shortcut(p=None, make=True)
- copy(word, tab=0)
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
