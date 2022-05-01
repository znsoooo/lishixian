"""Document Operation"""

import os
import csv


def _wash(cell):
    if isinstance(cell, float) and cell.is_integer():
        cell = int(cell)
    return str(cell)


__all__ = list(globals())


# ---------------------------------------------------------------------------
# Text
# ---------------------------------------------------------------------------


def WriteTxt(data, file, encoding='utf-8-sig'):
    with open(file, 'w', encoding=encoding) as f:
        f.write('\n'.join(','.join(str(cell) for cell in row) for row in data))


def ReadCsv(file, encoding='utf-8-sig'):
    with open(file, encoding=encoding) as f:
        return list(csv.reader(f))


def WriteCsv(data, file, encoding='utf-8-sig', errors='ignore'):
    with open(file, 'w', newline='', encoding=encoding, errors=errors) as f:
        writer = csv.writer(f)
        writer.writerows(data)


# ---------------------------------------------------------------------------
# Excel
# ---------------------------------------------------------------------------


def WriteExcel(data, file, new_sheet='sheet1'):
    import xlwt
    xls = xlwt.Workbook('u8')
    sheet = xls.add_sheet(new_sheet, True)
    for r, row in enumerate(data):
        for c, cell in enumerate(row):
            sheet.write(r, c, cell)
    xls.save(file)


def OpenExcel(file):
    import xlrd
    import xlutils.filter

    rb = xlrd.open_workbook(file, formatting_info=True)

    # 参考xlutils.copy库内的用法 参考xlutils.filter内的参数定义style_list
    w = xlutils.filter.XLWTWriter()
    xlutils.filter.process(xlutils.filter.XLRDReader(rb, 'unknown.xls'), w)
    wb = w.output[0][1]
    wb.style_list = w.style_list
    wb.sheets = rb.sheets()

    # quick `style` reach, and `write` with copied style.
    wb.style = lambda n, r, c: wb.style_list[wb.sheets[n].cell_xf_index(r, c)]
    wb.swrite = lambda n, r, c, value: wb.get_sheet(n).write(r, c, value, wb.style(n, r, c))

    return wb


def MergeCell(data, merge, merge_x=True, merge_y=True, strip_x=False):
    data2 = []
    for sheet_data, sheet_merge in zip(data, merge):
        # merge cell
        for r1, r2, c1, c2 in sheet_merge:
            for r in range(r1, r2):
                for c in range(c1, c2):
                    if (not merge_x and c > c1) or (not merge_y and r > r1):
                        sheet_data[r][c] = None if strip_x else ''
                    else:
                        sheet_data[r][c] = sheet_data[r1][c1]
        # strip x
        if strip_x:
            sheet_data = [[cell for cell in row if cell is not None] for row in sheet_data]
        data2.append(sheet_data)
        # remove blanks in tail
        # for row in sheet_data:
        #     while len(row) and row[-1] == '':  # Good!
        #         row.pop()
    return data2


def ReadExcel(file, merge_x=True, merge_y=True, strip_x=False):
    import xlrd
    try:
        xls = xlrd.open_workbook(file, formatting_info=True)
    except xlrd.biffh.XLRDError:
        xls = xlrd.open_workbook(file)

    data = []
    for sheet in xls.sheets():
        sheet_name = sheet.name
        sheet_data = []
        for row in range(sheet.nrows):
            rows = [sheet_name] + sheet.row_values(row)
            sheet_data.append(list(map(_wash, rows)))
        data.append(sheet_data)

    # only ".xls" type contain merge_info
    merge = [sorted(sheet.merged_cells) for sheet in xls.sheets()]
    data2 = MergeCell(data, merge, merge_x, merge_y, strip_x)
    return data, merge


def ReadSheet(file, index=0):
    import xlrd
    xls = xlrd.open_workbook(file)
    sheet = xls.sheet_by_index(index)
    return [list(map(_wash, sheet.row_values(row))) for row in range(sheet.nrows)]


# ---------------------------------------------------------------------------
# Word
# ---------------------------------------------------------------------------


def Doc2Docx(file, overwrite=False):
    root, ext = os.path.splitext(file)
    file2 = root + '.docx.temp'
    if overwrite or not os.path.exists(file2):
        from win32com import client
        word = client.Dispatch('Word.Application')
        doc = word.Documents.Open(file)
        doc.SaveAs(file2, 16)
        doc.Close()
    return file2


def OpenDocx(file):
    import docx
    data = []
    merge = []
    doc = docx.Document(file)
    for table in doc.tables:
        cells  = table._cells  # see usage at `docx.table.Table._cells`
        cols   = table._column_count
        length = len(cells)

        # read text
        data.append([])
        for i, cell in enumerate(cells):
            r, c = divmod(i, cols)
            if c == 0:  # create new row
                data[-1].append([])
            data[-1][-1].append(cell.text)

        # find merged
        merge.append([])
        for i, cell in enumerate(cells):
            if cell in cells[:i]:  # only find first repeated cell
                continue
            for j in range(length - 1, 0, -1):  # find last repeated cell
                if cell is cells[j]:  # always can be found
                    break
            if i != j:  # first != last -> merged cells
                r1, c1 = divmod(i, cols)
                r2, c2 = divmod(j, cols)
                merge[-1].append((r1, r2 + 1, c1, c2 + 1))

    return data, merge


def ReadWordTexts(file):
    import docx
    if file.endswith('.doc'):
        file = Doc2Docx(file)
    doc = docx.Document(file)
    return [p.text for p in doc.paragraphs]


def ReadWord(file, merge_x=True, merge_y=True, strip_x=False):
    if file.endswith('.doc'):
        file = Doc2Docx(file)
    data, merge = OpenDocx(file)
    data2 = MergeCell(data, merge, merge_x, merge_y, strip_x)
    return data2


# ---------------------------------------------------------------------------
# Other
# ---------------------------------------------------------------------------


def ReadFile(file, merge_x=True, merge_y=True, strip_x=False):
    ext = os.path.splitext(file)[1]
    if ext in ('.csv', '.txt'):
        return ReadCsv(file)
    elif ext in ('.xls', '.xlsx'):
        return ReadExcel(file, merge_x, merge_y, strip_x)
    elif ext in ('.doc', '.docx'):
        return ReadWord(file, merge_x, merge_y, strip_x)


def File2Csv(file, merge_x=True, merge_y=True, strip_x=False):
    root, ext = os.path.splitext(file)
    data = ReadFile(file, merge_x, merge_y, strip_x)
    WriteCsv(data, root + '.csv')
    return data


def ReadFiles(files, merge_x=True, merge_y=True, strip_x=False):
    data = []
    for file in files:
        path, filename = os.path.split(file)
        data.extend([[path, filename] + row for row in ReadFile(file, merge_x, merge_y, strip_x)])
    return data


def Unique(arr):
    return [i for i, item in enumerate(arr) if arr.index(item) == i]


__all__ = [k for k in globals() if k not in __all__]


if __name__ == '__main__':
    from pprint import pprint

    # test read
    data = ReadExcel('../test.xls')
    # pprint(data)

    pprint(ReadWord('../test.docx', False, False, False))
    pprint(ReadWord('../test.docx', False, True,  False))
    pprint(ReadWord('../test.docx', True,  False, False))
    pprint(ReadWord('../test.docx', True,  True,  False))

    # test read/write with keep style
    wb = OpenExcel('../test2.xls')
    sheet2 = wb.get_sheet(0)
    for r in range(3):
        for c in range(3):
            sheet2.write(r, c, 'T%d%d' % (r, c), wb.style(0, r, c))
            # wb.swrite(0, r, c, 'V%d%d' % (r, c))

    wb.save('save2.xls')
