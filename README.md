# Lishixian Library
Contain 92 functions.


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
- help()

### Module 'cls'
- MyConfigParser(path, section)
- MyThread(target, *args, **kwargs)
- Tcp(addr='localhost', port=7010)

### Module 'decorator'
- timeit(f)
- tracer(f)
- protect(f)
- surround(before=(), after=())

### Module 'line'
- s128 = bytes(range(128)).decode()
- s127 = bytes(range(32, 127)).decode()
- empty(*v, **kv)
- t(arr)
- md5(b)
- start(func, *args, **kwargs)
- create(file)
- pprint(*value, file=sys.stdout)
- dumps(data)
- sort_kv(d, reverse=False)
- sort_key(d, reverse=False)
- sort_num(s)
- raw2headers(s)
- str2dict(s)
- unique(p, dash='-')
- pc_ip()
- pc_mac()
- pc_user()
- randombytes(n)
- tuple2item(item)
- join(path, *paths)

### Module 'refact'
- infinity = <class 'itertools.count'>
- makedirs(name, mode=511, *, exist_ok=True)
- breakpoint()
- popen(cmd)
- listdir(*paths)
- findall(pattern, string, flags=0)
- split(arr, cols)
- print(*value, **kwargs)
- splitpath(p)
- walk(path, exts=())
- open(file)

### Module 'useful'
- tag()
- log(*value)
- check(obj, rule=<class 'bool'>)
- safe_name(filename, repl=' ')
- escape(s, quote=True)
- unescape(s)
- quote(string, safe='', encoding=None, errors=None)
- unquote(string, encoding='utf-8', errors='replace')
- urlopen(url, timeout=5)
- findpair(s, p1='(', p2=')', st=0)
- bytes_format(data, n=16)
- bytes_print(data, n=16)
- bytes_hex(data, offset=0, length=-1, slice=-1)
- argv_run(func, *defaults)
- install(path, block=False)
- input_wait(msg)
- input_default(msg, default)
- Catch(log='log.txt')
- catch = <Catch object>
- MaxThread(max)

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
- WriteTxt(data, file, encoding='utf-8-sig')
- ReadCsv(file, encoding='utf-8-sig')
- WriteCsv(data, file, encoding='utf-8-sig', errors='ignore')
- WriteExcel(data, file, new_sheet='sheet1')
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
- Unique(arr)

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
